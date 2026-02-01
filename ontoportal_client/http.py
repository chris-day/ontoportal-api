from __future__ import annotations

import json
import logging
import time
from typing import Any

import requests

from .config import ClientConfig
from .exceptions import ApiError, AuthError, RateLimitError


class HttpClient:
    def __init__(self, config: ClientConfig, logger: logging.Logger | None = None):
        self.config = config
        self.session = requests.Session()
        self.logger = logger or logging.getLogger("ontoportal")
        self.session.headers.update({"User-Agent": self.config.user_agent})

    def request(self, method: str, path: str, *, params: dict | None = None, json_body: Any = None):
        url = self._build_url(path)
        return self._request_url(method, url, params=params, json_body=json_body)

    def request_url(
        self, method: str, url: str, *, params: dict | None = None, json_body: Any = None
    ):
        return self._request_url(method, url, params=params, json_body=json_body)

    def _build_url(self, path: str) -> str:
        base = self.config.base_url.rstrip("/")
        if not path.startswith("/"):
            path = "/" + path
        return base + path

    def _apply_auth(self, params: dict, headers: dict):
        if not self.config.api_key:
            return
        if self.config.auth_mode == "query":
            params.setdefault("apikey", self.config.api_key)
        else:
            headers.setdefault("Authorization", f"apikey token={self.config.api_key}")

    def _request_url(
        self, method: str, url: str, *, params: dict | None = None, json_body: Any = None
    ):
        params = dict(params or {})
        headers = {}
        self._apply_auth(params, headers)

        attempts = self.config.max_retries + 1
        last_error: Exception | None = None

        for attempt in range(attempts):
            start = time.time()
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_body,
                    headers=headers,
                    timeout=self.config.timeout_s,
                )
            except requests.RequestException as exc:
                last_error = exc
                break

            duration_ms = int((time.time() - start) * 1000)
            request_id = response.headers.get("X-Request-Id")
            self.logger.info(
                "HTTP %s %s -> %s (%sms) req_id=%s",
                method.upper(),
                response.url,
                response.status_code,
                duration_ms,
                request_id,
            )

            if response.status_code in (401, 403):
                raise AuthError(response.status_code, self._error_message(response))

            if response.status_code == 429:
                retry_after = self._retry_after_seconds(response)
                if attempt >= self.config.max_retries:
                    raise RateLimitError(
                        response.status_code,
                        self._error_message(response),
                        retry_after_s=retry_after,
                    )
                self._sleep_with_backoff(attempt, retry_after)
                continue

            if 200 <= response.status_code < 300:
                return self._parse_json(response)

            raise ApiError(response.status_code, self._error_message(response), self._error_payload(response))

        if last_error:
            raise ApiError(0, f"Network error: {last_error}")

        raise ApiError(0, "Request failed")

    def _parse_json(self, response: requests.Response):
        if not response.text:
            return None
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise ApiError(response.status_code, f"Invalid JSON response: {exc}")

    def _error_payload(self, response: requests.Response) -> dict:
        try:
            payload = response.json()
            return payload if isinstance(payload, dict) else {"error": payload}
        except json.JSONDecodeError:
            return {"error": response.text}

    def _error_message(self, response: requests.Response) -> str:
        payload = self._error_payload(response)
        if isinstance(payload, dict):
            return payload.get("message") or payload.get("error") or response.reason
        return response.reason

    def _retry_after_seconds(self, response: requests.Response) -> float | None:
        header = response.headers.get("Retry-After")
        if not header:
            return None
        try:
            return float(header)
        except ValueError:
            return None

    def _sleep_with_backoff(self, attempt: int, retry_after: float | None):
        if retry_after is not None:
            time.sleep(retry_after)
            return
        backoff = min(
            self.config.backoff_max_s,
            self.config.backoff_initial_s * (2**attempt),
        )
        time.sleep(backoff)

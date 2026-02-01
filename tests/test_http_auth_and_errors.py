import json
from unittest.mock import Mock

import pytest

from ontoportal_client.config import ClientConfig
from ontoportal_client.http import HttpClient
from ontoportal_client.exceptions import AuthError, RateLimitError


class FakeResponse:
    def __init__(self, status_code=200, payload=None, headers=None, url="https://x"):
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}
        self.url = url
        self.reason = "ERR"

    @property
    def text(self):
        if self._payload is None:
            return ""
        return json.dumps(self._payload)

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


def test_auth_header_applied():
    config = ClientConfig(api_key="abc", auth_mode="header")
    http = HttpClient(config)
    http.session.request = Mock(return_value=FakeResponse(payload={"ok": True}))

    http.request("GET", "/ontologies")

    _, kwargs = http.session.request.call_args
    headers = kwargs.get("headers")
    assert headers["Authorization"] == "apikey token=abc"


def test_auth_query_param_applied():
    config = ClientConfig(api_key="abc", auth_mode="query")
    http = HttpClient(config)
    http.session.request = Mock(return_value=FakeResponse(payload={"ok": True}))

    http.request("GET", "/ontologies")

    _, kwargs = http.session.request.call_args
    params = kwargs.get("params")
    assert params["apikey"] == "abc"


def test_401_raises_auth_error():
    config = ClientConfig(api_key="abc")
    http = HttpClient(config)
    http.session.request = Mock(return_value=FakeResponse(status_code=401, payload={"message": "no"}))

    with pytest.raises(AuthError):
        http.request("GET", "/ontologies")


def test_429_retries_then_rate_limit_error():
    config = ClientConfig(api_key="abc", max_retries=1, backoff_initial_s=0, backoff_max_s=0)
    http = HttpClient(config)
    http.session.request = Mock(
        side_effect=[
            FakeResponse(status_code=429, payload={"message": "rate"}, headers={"Retry-After": "0"}),
            FakeResponse(status_code=429, payload={"message": "rate"}, headers={"Retry-After": "0"}),
        ]
    )

    with pytest.raises(RateLimitError):
        http.request("GET", "/ontologies")

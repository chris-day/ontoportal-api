from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import os


@dataclass(frozen=True)
class ClientConfig:
    base_url: str = "https://data.bioontology.org"
    api_key: str | None = None
    auth_mode: str = "header"  # "header" or "query"
    timeout_s: float = 30.0
    max_retries: int = 3
    backoff_initial_s: float = 0.5
    backoff_max_s: float = 8.0
    user_agent: str = "ontoportal-client/1.0"

    @classmethod
    def from_env(cls, prefix: str = "ONTOPORTAL") -> "ClientConfig":
        key = os.getenv(f"{prefix}_API_KEY")
        auth_mode = os.getenv(f"{prefix}_AUTH_MODE", "header")
        base_url = os.getenv(f"{prefix}_BASE_URL", cls.base_url)
        timeout_s = float(os.getenv(f"{prefix}_TIMEOUT_S", cls.timeout_s))
        max_retries = int(os.getenv(f"{prefix}_MAX_RETRIES", cls.max_retries))
        backoff_initial_s = float(
            os.getenv(f"{prefix}_BACKOFF_INITIAL_S", cls.backoff_initial_s)
        )
        backoff_max_s = float(os.getenv(f"{prefix}_BACKOFF_MAX_S", cls.backoff_max_s))
        user_agent = os.getenv(f"{prefix}_USER_AGENT", cls.user_agent)
        return cls(
            base_url=base_url,
            api_key=key,
            auth_mode=auth_mode,
            timeout_s=timeout_s,
            max_retries=max_retries,
            backoff_initial_s=backoff_initial_s,
            backoff_max_s=backoff_max_s,
            user_agent=user_agent,
        )

    @classmethod
    def from_file(cls, path: str | Path) -> "ClientConfig":
        raw = Path(path).read_text(encoding="utf-8")
        data = json.loads(raw)
        return cls(**data)

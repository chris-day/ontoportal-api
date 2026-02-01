class ApiError(RuntimeError):
    def __init__(self, status_code: int, message: str, details: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


class AuthError(ApiError):
    pass


class RateLimitError(ApiError):
    def __init__(self, status_code: int, message: str, retry_after_s: float | None = None):
        super().__init__(status_code, message)
        self.retry_after_s = retry_after_s

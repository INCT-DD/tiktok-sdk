"""Exceptions raised by Research API requests."""


class QueryException(Exception):
    """Report a transport or TikTok API failure with its available details."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
        log_id: str | None = None,
    ) -> None:
        """Keep the error message, HTTP status, TikTok error code, and log ID.

        A connection failure has no HTTP status. Some responses omit the
        TikTok code or log ID.
        """
        super().__init__(f"{code}: {message}" if code and code != message else message)
        self.status_code = status_code
        self.code = code
        self.log_id = log_id

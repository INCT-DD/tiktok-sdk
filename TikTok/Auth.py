"""
Provides OAuth2 authentication functionality for the TikTok API. It handles the
OAuth2 flow, including obtaining and refreshing access tokens automatically.

The main class, OAuth2, manages the authentication process and token lifecycle. It supports
automatic token refresh when the current token is about to expire, and persists tokens to disk
for reuse across sessions.

Usage:
    To use this module, create an instance of the OAuth2 class using the `authenticate` class method:

    ```python
    from TikTok.Auth import OAuth2
    from TikTok.ValidationModels.OAuth2 import RequestHeadersModel, TokenRequestBodyModel

    auth: OAuth2 = await OAuth2.authenticate(
        headers=RequestHeadersModel(),
        body=TokenRequestBodyModel(
            client_key="YOUR_CLIENT_KEY",
            client_secret="YOUR_CLIENT_SECRET",
        ),
    )
    ```
"""

import asyncio
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import time

import httpx
import orjson
import stamina
import structlog

from TikTok.ValidationModels.RestAPI import APIEndpoints
from TikTok.Exceptions.Auth import AuthException
from TikTok.ValidationModels.OAuth2 import (
    RequestHeadersModel,
    TokenRequestBodyModel,
    OAuth2ResponseModel,
    OAuth2Token,
)

logger = structlog.get_logger()


class OAuth2:
    """
    Handles OAuth2 authentication for TikTok API.

    This class manages the OAuth flow, including obtaining and refreshing access tokens.

    Attributes:
        headers (RequestHeadersModel): Headers for the OAuth request.
        body (TokenRequestBodyModel): Body parameters for the OAuth request.
        _oauth2_token (OAuth2Token | None): The current access token.
        client (httpx.AsyncClient): An asynchronous HTTP client for making requests.
    """

    headers: RequestHeadersModel
    body: TokenRequestBodyModel
    client: httpx.AsyncClient

    def __init__(
        self, headers: RequestHeadersModel, body: TokenRequestBodyModel
    ) -> None:
        """
        Initialize the OAuth instance.

        Args:
            headers (RequestHeadersModel): Headers for the OAuth request.
            body (TokenRequestBodyModel): Body parameters for the OAuth request.
        """
        self.headers = headers
        self.body = body
        self.client = httpx.AsyncClient(http2=True)
        self._refresh_lock = asyncio.Lock()
        self._oauth2_token: OAuth2Token | None = None
        key = sha256(body.client_key.encode()).hexdigest()
        self._cache_file = Path.home() / ".cache" / "tiktok-sdk" / f"{key}.json"

    def _load_cached_token(self) -> OAuth2Token | None:
        """Read the token for this client key, or return None if it is unavailable."""
        try:
            return OAuth2Token.model_validate_json(self._cache_file.read_bytes())
        except FileNotFoundError:
            return None
        except OSError, ValueError:
            logger.warning("Could not read the cached access token.")
            return None

    def _save_cached_token(self, token: OAuth2Token) -> None:
        """Replace the cache file atomically. A write failure leaves the token usable."""
        try:
            self._cache_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with NamedTemporaryFile(
                dir=self._cache_file.parent, delete_on_close=False
            ) as temp:
                temp.write(token.model_dump_json().encode())
                temp.close()
                Path(temp.name).replace(self._cache_file)
        except OSError as exc:
            logger.warning("Could not save the access token.", error=str(exc))

    @stamina.retry(on=AuthException, attempts=5)
    async def _request_access_token(self) -> OAuth2Token:
        """Request a token. Raise AuthException after five failed OAuth attempts."""
        response = await self.client.post(
            url=APIEndpoints().OAuthTokenRequestURL,
            headers=self.headers.model_dump(by_alias=True),
            data=self.body.model_dump(),
        )
        if response.status_code != 200:
            logger.error(
                "Access token request failed.", status_code=response.status_code
            )
            raise AuthException(f"Failed to obtain access token: {response.text}")

        payload = orjson.loads(response.content)
        match payload:
            case {"error": error}:
                logger.error("Access token request failed.", error=error)
                raise AuthException(f"Failed to obtain access token: {error}")

        token = OAuth2ResponseModel.model_validate(payload)
        logger.info("Access token obtained.")
        return OAuth2Token(
            access_token=token.access_token,
            token_type=token.token_type,
            expires_at=datetime.now(UTC) + timedelta(seconds=token.expires_in),
        )

    async def get_access_token(self) -> str:
        """Return the access token. Refresh it when 60 seconds or less remain.

        Concurrent requests on this instance share one refresh. An OAuth error
        raises AuthException. Invalid response data raises ValueError. A
        connection failure raises httpx.RequestError.
        """
        async with self._refresh_lock:
            if self._oauth2_token is None:
                self._oauth2_token = await asyncio.to_thread(self._load_cached_token)
            if (
                self._oauth2_token is None
                or self._oauth2_token.expires_at.timestamp() <= time() + 60
            ):
                self._oauth2_token = await self._request_access_token()
                await asyncio.to_thread(self._save_cached_token, self._oauth2_token)
            return self._oauth2_token.access_token

    @classmethod
    async def authenticate(
        cls, headers: RequestHeadersModel, body: TokenRequestBodyModel
    ) -> OAuth2:
        """Create an OAuth client and obtain a token for the supplied credentials.

        Return the authenticated client. If token acquisition fails, close the
        HTTP client and propagate the error.
        """
        instance = cls(headers, body)
        try:
            await instance.get_access_token()
        except BaseException:
            await instance.client.aclose()
            raise
        return instance

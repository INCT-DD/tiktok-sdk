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
    from TikTok.Types.OAuth2 import RequestHeadersModel, TokenRequestBodyModel

    auth: OAuth2 = await OAuth2.authenticate(
        headers=RequestHeadersModel(),
        body=TokenRequestBodyModel(
            client_key="YOUR_CLIENT_KEY",
            client_secret="YOUR_CLIENT_SECRET",
        ),
    )
    ```
"""

import httpx
import orjson
import stamina
import structlog
from typing import Self
from datetime import datetime, timedelta
import pickle
from pathlib import Path

from TikTok.Types.RestAPI import APIEndpoints
from TikTok.Exceptions.Auth import AuthException
from TikTok.Types.OAuth2 import RequestHeadersModel, TokenRequestBodyModel, OAuth2Token

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
    _oauth2_token: OAuth2Token | None = None
    client: httpx.AsyncClient

    def __init__(self, headers: RequestHeadersModel, body: TokenRequestBodyModel):
        """
        Initialize the OAuth instance.

        Args:
            headers (RequestHeadersModel): Headers for the OAuth request.
            body (TokenRequestBodyModel): Body parameters for the OAuth request.
        """
        self.headers = headers
        self.body = body
        self.client = httpx.AsyncClient(http2=True)

    @stamina.retry(on=AuthException, attempts=5)
    async def _request_access_token(self) -> None:
        """
        Obtain a new access token from the TikTok API or load from disk if available.

        This method first attempts to load the token from disk. If unsuccessful, it sends
        a POST request to the OAuth token endpoint and processes the response.

        Returns:
            None

        Raises:
            AuthException: If the request fails or the response is invalid.
        """
        token_file: Path = Path("token.pkl")

        if self._oauth2_token is None and token_file.exists():
            try:
                with open(token_file, "rb") as f:
                    self._oauth2_token = pickle.load(f)
                logger.info("Access token loaded from disk.")
                if (
                    self._oauth2_token.expires_at - datetime.now()
                ).total_seconds() > 60:
                    return
            except Exception as e:
                logger.error(f"Failed to load token from disk: {e}")

        response: httpx.Response = await self.client.post(
            url=APIEndpoints().OAuthTokenRequestURL,
            headers=self.headers.model_dump(),
            data=self.body.model_dump(),
        )

        if response.status_code == 200:
            response_data: dict[str, str | int] = orjson.loads(response.content)

            if "error" in response_data:
                logger.error(f"Failed to obtain access token: {response_data['error']}")
                raise AuthException(
                    f"Failed to obtain access token: {response_data['error']}"
                )

            logger.info("Access token obtained.")
            expires_in: int = int(response_data["expires_in"])
            self._oauth2_token = OAuth2Token(
                access_token=response_data["access_token"],
                token_type=response_data["token_type"],
                expires_at=datetime.now() + timedelta(seconds=expires_in),
            )

            # Serialize token to disk
            try:
                with open(token_file, "wb") as f:
                    pickle.dump(self._oauth2_token, f)
                logger.info("Access token saved to disk.")
            except Exception as e:
                logger.error(f"Failed to save token to disk: {e}")
        else:
            logger.error(f"Failed to obtain access token: {response.text}")
            raise AuthException(f"Failed to obtain access token: {response.text}")

    async def get_access_token(self) -> str:
        """
        Retrieve the current access token.

        This method checks if the access token is still valid. If the token is about to expire
        in less than 60 seconds, it requests a new token.

        Returns:
            str: The current access token.

        Raises:
            Exception: If the access token cannot be obtained.
        """
        if (
            self._oauth2_token.expires_at
            and (self._oauth2_token.expires_at - datetime.now()).total_seconds() < 60
        ):
            await self._request_access_token()
        return self._oauth2_token.access_token

    @classmethod
    async def authenticate(
        cls, headers: RequestHeadersModel, body: TokenRequestBodyModel
    ) -> "OAuth2":
        """
        Create and authenticate a new OAuth instance.

        This class method creates a new OAuth instance, initializes it with the provided
        headers and body, and obtains an access token.

        Args:
            headers (RequestHeadersModel): Headers for the OAuth request.
            body (TokenRequestBodyModel): Body parameters for the OAuth request.

        Returns:
            OAuth2: An authenticated OAuth instance with a valid access token.

        Raises:
            Exception: If authentication fails or the access token cannot be obtained.
        """
        instance: Self = cls(headers, body)
        await instance._request_access_token()
        return instance

"""
Defines models and enumerations for handling OAuth2 authentication in the TikTok API.

The models in this module are designed to facilitate the OAuth2 authentication process by providing
structured representations of the various components involved, such as grant types, token types,
request headers, and token request/response bodies. These models ensure that the data used in OAuth2
requests and responses is validated and correctly formatted, reducing the risk of errors when interacting
with the API.
"""

from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from TikTok.ValidationModels.BaseModels import NoExtraFieldsBaseModel, HeadersModel


class OAuth2GrantType(StrEnum):
    """
    Enumeration for OAuth2 grant types.

    This enumeration defines the different types of OAuth2 grants that can be used
    in the OAuth2 authentication process.

    Attributes:
        client_credentials (str): Represents the client credentials grant type.
    """

    client_credentials = "client_credentials"


class OAuth2TokenType(StrEnum):
    """
    Enumeration for OAuth2 token types.

    This enumeration defines the different types of tokens that can be used
    in the OAuth2 authentication process.

    Attributes:
        bearer (str): Represents the Bearer token type.
    """

    bearer = "Bearer"


class RequestHeadersModel(HeadersModel):
    """
    Model representing the request headers for OAuth2 requests.

    This model defines the standard headers that are typically included
    in OAuth2 requests, with default values for content type and cache control.
    The field names use aliases to match the exact HTTP header names.

    Attributes:
        content_type (str): The content type of the request, defaulting to
            "application/x-www-form-urlencoded".
        cache_control (str): The cache control directive, defaulting to
            "no-cache".
    """

    content_type: str = Field(
        default="application/x-www-form-urlencoded", alias="Content-Type"
    )
    cache_control: str = Field(default="no-cache", alias="Cache-Control")


class AuthorizationHeaderModel(HeadersModel):
    """
    Model representing the authorization header for OAuth2 requests.

    This model extends the HeadersModel to include the authorization field,
    which is essential for making authenticated requests to the OAuth2 API.

    Attributes:
        authorization (str): The authorization token, typically prefixed with "Bearer ".
    """

    authorization: str = Field(alias="Authorization")

    @field_validator("authorization", mode="before")
    @classmethod
    def prepend_bearer(cls, value: str) -> str:
        """
        Prepend 'Bearer ' to the authorization value if it's not already present.

        This method ensures that the authorization token is correctly formatted
        for OAuth2 requests by adding the "Bearer " prefix when necessary.

        Args:
            value (str): The original authorization value.

        Returns:
            str: The authorization value with 'Bearer ' prepended if necessary.
        """
        return f"Bearer {value}" if not value.startswith("Bearer ") else value


class TokenRequestBodyModel(NoExtraFieldsBaseModel):
    """
    Model representing the body of a token request for OAuth2.

    This model encapsulates the necessary parameters required to request
    an access token using the client credentials grant type.

    Attributes:
        client_key (str): The client key provided by the OAuth2 provider.
        client_secret (str): The client secret provided by the OAuth2 provider.
        grant_type (OAuth2GrantType): The type of grant being requested, which is fixed to "client_credentials".
    """

    client_key: str
    client_secret: str
    grant_type: OAuth2GrantType = Field(
        default=OAuth2GrantType.client_credentials, frozen=True
    )


class OAuth2ResponseModel(BaseModel):
    """
    Model representing the response from an OAuth2 token request.

    This model captures the details returned by the OAuth2 provider after
    a successful token request.

    Attributes:
        access_token (str): The access token issued by the OAuth2 provider.
        expires_in (int): The duration in seconds for which the access token
            is valid.
        token_type (OAuth2TokenType): The type of the token issued (e.g., "Bearer").
    """

    access_token: str
    expires_in: int
    token_type: OAuth2TokenType


class OAuth2Token(NoExtraFieldsBaseModel):
    """
    Model representing an OAuth2 token.

    This model encapsulates the access token, its expiration time, and the token type.

    Attributes:
        access_token (str): The access token issued by the OAuth2 provider.
        expires_at (datetime): The exact datetime when the access token will expire.
        token_type (OAuth2TokenType): The type of the token issued (e.g., "Bearer").
    """

    access_token: str
    expires_at: datetime
    token_type: OAuth2TokenType

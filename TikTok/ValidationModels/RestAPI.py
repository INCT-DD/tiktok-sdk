"""
Defines the structure and configuration for interacting with the TikTok API.

It includes enumerations and models that encapsulate the base API configuration and specific API endpoints.
"""

from enum import StrEnum
from pydantic import HttpUrl
from TikTok.ValidationModels.BaseModels import NoExtraFieldsBaseModel


class BaseAPI(StrEnum):
    """
    Enumeration for the base API configuration.

    This class defines the base URL and API version for the TikTok API.
    It provides a structured way to access these constants throughout the
    application.

    Attributes:
        base_url (HttpUrl): The base URL for the TikTok API.
        api_version (str): The version of the TikTok API being used.
    """

    base_url: HttpUrl = "https://open.tiktokapis.com"
    api_version: str = "v2"


class APIEndpoints(NoExtraFieldsBaseModel):
    """
    Model representing the API endpoints for the TikTok API.

    This model encapsulates the various endpoints used to interact with the TikTok API,
    providing a structured way to access the URLs required for OAuth token requests and
    user information retrieval.

    Attributes:
        OAuthTokenRequestURL (HttpUrl): The URL for requesting an OAuth token.
        UserInfoURL (HttpUrl): The URL for retrieving user information.
    """

    OAuthTokenRequestURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/oauth/token/"
    )
    UserInfoURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/user/info/"
    )
    PlaylistInfoURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/playlist/info/"
    )

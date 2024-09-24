"""
Defines the structure and configuration of the TikTok API.

This module includes enumerations and models that encapsulate the base API configuration,
specific API endpoints, and their respective URLs for interacting with the TikTok API.
It serves as a foundation for making requests to the TikTok API, ensuring a structured
and consistent approach to accessing API resources.
"""

from enum import StrEnum
from pydantic import HttpUrl
from TikTok.ValidationModels.BaseModels import BaseRequestModel


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


class APIEndpoints(BaseRequestModel):
    """
    Model representing the API endpoints for the TikTok API.

    This model encapsulates the various endpoints used to interact with the TikTok API,
    providing a structured way to access the URLs required for OAuth token requests, user
    information retrieval, and other actions.

    Attributes:
        OAuthTokenRequestURL (HttpUrl): The URL for requesting an OAuth token.
        UserInfoURL (HttpUrl): The URL for retrieving user information.
        UserLikedVideosURL (HttpUrl): The URL for retrieving videos liked by a user.
        UserPinnedVideosURL (HttpUrl): The URL for retrieving videos pinned by a user.
        UserRepostedVideosURL (HttpUrl): The URL for retrieving videos reposted by a user.
        UserFollowingURL (HttpUrl): The URL for retrieving users that a specified user is following.
        UserFollowersURL (HttpUrl): The URL for retrieving followers of a specified user.
        PlaylistInfoURL (HttpUrl): The URL for retrieving information about a specific playlist.
        VideoSearchURL (HttpUrl): The URL for searching videos based on specified criteria.
    """

    OAuthTokenRequestURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/oauth/token/"
    )
    UserInfoURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/user/info/"
    )
    UserLikedVideosURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/user/liked_videos/"
    )
    UserPinnedVideosURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/user/pinned_videos/"
    )
    UserRepostedVideosURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/user/reposted_videos/"
    )
    UserFollowingURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/user/following/"
    )
    UserFollowersURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/user/followers/"
    )
    PlaylistInfoURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/playlist/info/"
    )
    VideoSearchURL: HttpUrl = (
        f"{BaseAPI.base_url}/{BaseAPI.api_version}/research/video/query/"
    )

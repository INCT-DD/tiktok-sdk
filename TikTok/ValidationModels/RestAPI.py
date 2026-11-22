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


_API_ROOT = f"{BaseAPI.base_url}/{BaseAPI.api_version}"
_RESEARCH_ROOT = f"{_API_ROOT}/research"


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
        VideoCommentsURL (HttpUrl): Comments for a video or replies to a comment.
        ComplianceCreateURL (HttpUrl): Submit a batch of video or comment IDs.
        ComplianceStatusURL (HttpUrl): Check the state of a submitted task.
        ComplianceDownloadURL (HttpUrl): Download the valid IDs from a completed task.
        ShopInfoURL (HttpUrl): Find EU shops by name.
        ShopProductsURL (HttpUrl): Get a page of products from a shop.
        ShopReviewsURL (HttpUrl): Get a page of reviews for a product.
    """

    OAuthTokenRequestURL: HttpUrl = f"{_API_ROOT}/oauth/token/"
    UserInfoURL: HttpUrl = f"{_RESEARCH_ROOT}/user/info/"
    UserLikedVideosURL: HttpUrl = f"{_RESEARCH_ROOT}/user/liked_videos/"
    UserPinnedVideosURL: HttpUrl = f"{_RESEARCH_ROOT}/user/pinned_videos/"
    UserRepostedVideosURL: HttpUrl = f"{_RESEARCH_ROOT}/user/reposted_videos/"
    UserFollowingURL: HttpUrl = f"{_RESEARCH_ROOT}/user/following/"
    UserFollowersURL: HttpUrl = f"{_RESEARCH_ROOT}/user/followers/"
    PlaylistInfoURL: HttpUrl = f"{_RESEARCH_ROOT}/playlist/info/"
    VideoSearchURL: HttpUrl = f"{_RESEARCH_ROOT}/video/query/"
    VideoCommentsURL: HttpUrl = f"{_RESEARCH_ROOT}/video/comment/list/"
    ComplianceCreateURL: HttpUrl = f"{_RESEARCH_ROOT}/validation_task/create/"
    ComplianceStatusURL: HttpUrl = f"{_RESEARCH_ROOT}/validation_task_status/get/"
    ComplianceDownloadURL: HttpUrl = f"{_RESEARCH_ROOT}/validation_task/download/"
    ShopInfoURL: HttpUrl = f"{_RESEARCH_ROOT}/tts/shop/"
    ShopProductsURL: HttpUrl = f"{_RESEARCH_ROOT}/tts/product/"
    ShopReviewsURL: HttpUrl = f"{_RESEARCH_ROOT}/tts/review/"

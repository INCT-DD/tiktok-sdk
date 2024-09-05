"""
Defines models and enumerations related to user information in the TikTok API.
"""

from enum import StrEnum
from pydantic import BaseModel, Field
from TikTok.Types.Common import ResponseErrorModel
from TikTok.Types.BaseModels import NoExtraFieldsBaseModel
from TikTok.Types.OAuth2 import AuthorizationHeaderModel


class QueryFields(StrEnum):
    """
    Enumeration of query fields for user information.

    Attributes:
        display_name (str): User's display name.
        bio_description (str): User's bio description.
        avatar_url (str): URL of the user's avatar.
        is_verified (str): Verification status of the user.
        follower_count (str): Number of followers.
        following_count (str): Number of users being followed.
        likes_count (str): Number of likes received.
        video_count (str): Number of videos posted.
    """

    display_name = "display_name"
    bio_description = "bio_description"
    avatar_url = "avatar_url"
    is_verified = "is_verified"
    follower_count = "follower_count"
    following_count = "following_count"
    likes_count = "likes_count"
    video_count = "video_count"


RequestHeadersModel = AuthorizationHeaderModel


class ResponseDataModel(NoExtraFieldsBaseModel):
    """
    Model for user data in the API response.

    Attributes:
        display_name (str | None): User's display name.
        bio_description (str | None): User's bio description.
        avatar_url (str | None): URL of the user's avatar.
        is_verified (bool | None): Verification status of the user.
        follower_count (int | None): Number of followers.
        following_count (int | None): Number of users being followed.
        likes_count (int | None): Number of likes received.
        video_count (int | None): Number of videos posted.
    """

    display_name: str | None = Field(
        default=None, description="The user's display name / nickname"
    )
    bio_description: str | None = Field(
        default=None, description="The user's bio description"
    )
    avatar_url: str | None = Field(
        default=None, description="The url to a user's profile picture"
    )
    is_verified: bool | None = Field(
        default=None,
        description="The user's verified status. True if verified, false if not",
    )
    following_count: int | None = Field(
        default=None, description="The number of people the user is following"
    )
    follower_count: int | None = Field(
        default=None, description="The number of followers the user has"
    )
    video_count: int | None = Field(
        default=None, description="The number of videos posted"
    )
    likes_count: int | None = Field(
        default=None, description="The total number of likes the user has accumulated"
    )


class InfoRequestModel(NoExtraFieldsBaseModel):
    """
    Model for the user info request.

    Attributes:
        username (str): The username of the user to fetch information for.
    """

    username: str = Field(description="Username as the unique identifier")


class InfoResponseModel(BaseModel):
    """
    Model for the complete API response for user information.

    Attributes:
        data (ResponseDataModel): User data.
        error (ResponseErrorModel): Error information, if any.
    """

    data: ResponseDataModel
    error: ResponseErrorModel

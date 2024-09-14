"""
Defines models and enumerations related to user data in the TikTok API.
"""

from enum import StrEnum
from pydantic import BaseModel, Field
from TikTok.ValidationModels.Common import ResponseErrorModel
from TikTok.ValidationModels.BaseModels import NoExtraFieldsBaseModel
from TikTok.ValidationModels.OAuth2 import AuthorizationHeaderModel


class UserInfoQueryFields(StrEnum):
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


class LikedVideosQueryFields(StrEnum):
    """
    Enumeration of query fields for liked videos.

    Attributes:
        id (int64): The unique identifier of the TikTok video.
        create_time (int64): UTC Unix epoch (in seconds) of when the TikTok video was posted.
        username (str): The username as the unique identifier of the video creator.
        region_code (str): A two digit code for the country where the video creator registered their account.
        video_description (str): The description of the liked video.
        music_id (int64): The music ID used in the video.
        like_count (int64): The number of likes the video has received.
        comment_count (int64): The number of comments the video has received.
        share_count (int64): The number of shares the video has received.
        view_count (int64): The number of views the video has received.
        hashtag_names (list[str]): The list of hashtags used in the video.
        video_duration (int64): The duration of the video, in seconds.
        is_stem_verified (bool): Whether the video has been verified as being high quality STEM content.
        favorites_count (int64): The number of favorites that a video receives.
    """

    id = "id"
    create_time = "create_time"
    username = "username"
    region_code = "region_code"
    video_description = "video_description"
    music_id = "music_id"
    like_count = "like_count"
    comment_count = "comment_count"
    share_count = "share_count"
    view_count = "view_count"
    hashtag_names = "hashtag_names"
    video_duration = "video_duration"
    is_stem_verified = "is_stem_verified"
    favorites_count = "favorites_count"


UserInfoRequestHeadersModel = AuthorizationHeaderModel


class UserInfoResponseDataModel(NoExtraFieldsBaseModel):
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


class UserInfoRequestModel(NoExtraFieldsBaseModel):
    """
    Model for the user info request.

    Attributes:
        username (str): The username of the user to fetch information for.
    """

    username: str = Field(description="Username as the unique identifier")


class UserInfoResponseModel(BaseModel):
    """
    Model for the complete API response for user information.

    Attributes:
        data (ResponseDataModel): User data.
        error (ResponseErrorModel): Error information, if any.
    """

    data: UserInfoResponseDataModel
    error: ResponseErrorModel

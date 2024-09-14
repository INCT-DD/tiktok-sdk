"""
Defines models and enumerations related to liked videos in the TikTok API.
"""

from enum import StrEnum
from pydantic import BaseModel, Field
from TikTok.ValidationModels.Common import ResponseErrorModel
from TikTok.ValidationModels.BaseModels import NoExtraFieldsBaseModel
from TikTok.ValidationModels.OAuth2 import AuthorizationHeaderModel


class QueryFields(StrEnum):
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


class RequestHeadersModel(AuthorizationHeaderModel):
    """
    Model for request headers, extending AuthorizationHeaderModel.

    Attributes:
        content_type (str): The content type of the request, defaulting to "application/json".
    """

    content_type: str = Field(default="application/json", alias="Content-Type")


class LikedVideosRequestModel(NoExtraFieldsBaseModel):
    """
    Model for the request to retrieve liked videos of a user.

    This model encapsulates the parameters required to fetch the liked videos for a specific user on TikTok.

    Attributes:
        username (str): The unique identifier of the user whose liked videos are to be fetched.
        max_count (int | None): The maximum number of liked videos to return in a single response.
            The default is 20, with a maximum limit of 100. The actual number of videos returned may be
            fewer due to content moderation, deletion, or privacy settings.
        cursor (int | None): A Unix timestamp in UTC seconds indicating that only videos created on
            or before this time will be returned. The default value is set to the time the request is made.
    """

    username: str = Field(description="Username as the unique identifier")
    max_count: int | None = Field(
        default=None,
        description="The maximum number of liked videos in a single response. Default is 20, max is 100. It is possible that the API returns fewer videos than the max count due to content moderation outcomes, videos being deleted, marked as private by users, or more.",
    )
    cursor: int | None = Field(
        default=None,
        description="Videos created on or before this time will be returned. It is a Unix timestamp in UTC seconds. Default value is set as the time this request was made.",
    )


class UserLikedVideosDataModel(BaseModel):
    """
    Model representing liked video data response data in the API response.

    Attributes:
        id (int | None): The unique identifier of the TikTok video.
        create_time (int | None): UTC Unix epoch (in seconds) of when the TikTok video was posted.
        username (str | None): The username as the unique identifier of the video creator.
        region_code (str | None): A two digit code for the country where the video creator registered their account.
        video_description (str | None): The description of the liked video.
        music_id (int | None): The music ID used in the video.
        like_count (int | None): The number of likes the video has received.
        comment_count (int | None): The number of comments the video has received.
        share_count (int | None): The number of shares the video has received.
        view_count (int | None): The number of views the video has received.
        hashtag_names (list[str] | None): The list of hashtags used in the video.
        video_duration (int | None): The duration of the video, in seconds.
        is_stem_verified (bool | None): Whether the video has been verified as being high quality STEM content.
        favorites_count (int | None): The number of favorites that a video receives.
    """

    id: int | None = Field(
        default=None, description="The unique identifier of the TikTok video."
    )
    create_time: int | None = Field(
        default=None,
        description="UTC Unix epoch (in seconds) of when the TikTok video was posted.",
    )
    username: str | None = Field(
        default=None,
        description="The username as the unique identifier of the video creator.",
    )
    region_code: str | None = Field(
        default=None,
        description="A two digit code for the country where the video creator registered their account.",
    )
    video_description: str | None = Field(
        default=None, description="The description of the liked video."
    )
    music_id: int | None = Field(
        default=None, description="The music ID used in the video."
    )
    like_count: int | None = Field(
        default=None, description="The number of likes the video has received."
    )
    comment_count: int | None = Field(
        default=None, description="The number of comments the video has received."
    )
    share_count: int | None = Field(
        default=None, description="The number of shares the video has received."
    )
    view_count: int | None = Field(
        default=None, description="The number of views the video has received."
    )
    hashtag_names: list[str] | None = Field(
        default=None, description="The list of hashtags used in the video."
    )
    video_duration: int | None = Field(
        default=None, description="The duration of the video, in seconds."
    )
    is_stem_verified: bool | None = Field(
        default=None,
        description="Whether the video has been verified as being high quality STEM content.",
    )
    favorites_count: int | None = Field(
        default=None, description="The number of favorites that a video receives."
    )


class ResponseDataModel(BaseModel):
    """
    Model for the response data of liked videos.

    Attributes:
        cursor (int): A Unix timestamp in UTC seconds indicating where to start retrieving liked videos.
        has_more (bool): Indicates whether there are more liked videos available for retrieval.
        user_liked_videos (UserLikedVideosDataModel): The data model containing information about the user's liked videos.
    """

    cursor: int = Field(
        description="Retrieve liked videos starting from the specified Unix timestamp in UTC seconds"
    )
    has_more: bool = Field(description="Whether there are more liked videos or not")
    user_liked_videos: UserLikedVideosDataModel


class LikedVideosResponseModel(BaseModel):
    """
    Model for the complete API response for liked videos.

    Attributes:
        data (ResponseDataModel): User data.
        error (ResponseErrorModel): Error information, if any.
    """

    data: UserLikedVideosDataModel
    error: ResponseErrorModel

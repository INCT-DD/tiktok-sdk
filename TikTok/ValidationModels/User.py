"""
Defines models and enumerations related to user data in the TikTok API.
"""

from enum import StrEnum
from pydantic import BaseModel, Field
from TikTok.ValidationModels.BaseModels import ResponseErrorModel, BaseRequestModel


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


class UserVideosQueryFields(StrEnum):
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


class UserInfoResponseDataModel(BaseModel):
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


class UserInfoResponseModel(BaseModel):
    """
    Model for the complete API response for user information.

    Attributes:
        data (UserInfoResponseDataModel): User data.
        error (ResponseErrorModel): Error information, if any.
    """

    data: UserInfoResponseDataModel
    error: ResponseErrorModel


class BaseUserInfoRequestModel(BaseRequestModel):
    """
    Model for the user info request.

    Attributes:
        username (str): The username of the user to fetch information for.
    """

    username: str = Field(description="Username as the unique identifier")


class PaginatedUserInfoRequestModel(BaseUserInfoRequestModel):
    """
    Model for the paginated user info request.

    Attributes:
        max_count (int | None): The maximum number of users to return in a single response.
        cursor (int | None): A cursor for pagination, allowing retrieval of additional users.
    """

    max_count: int | None = Field(
        gt=0,
        le=100,
        default=None,
        description="The maximum number of results in a single response. Default is 20, max is 100. It is possible that the API returns fewer results than the max count due to content moderation outcomes, data being deleted, marked as private by users, or more.",
    )
    cursor: int | None = Field(
        default=None,
        description="Results created on or before this time will be returned. It is a Unix timestamp in UTC seconds. Default value is set as the time this request was made.",
    )


class UserVideosDataModel(BaseModel):
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


class UserLikedVideosResponseDataModel(BaseModel):
    """
    Model for the response data of liked videos.

    Attributes:
        cursor (int): A Unix timestamp in UTC seconds indicating where to start retrieving liked videos.
        has_more (bool): Indicates whether there are more liked videos available for retrieval.
        user_liked_videos (list[UserLikedVideosDataModel]): A list of data models containing information about the user's liked videos.
    """

    cursor: int = Field(
        description="Retrieve liked videos starting from the specified Unix timestamp in UTC seconds"
    )
    has_more: bool = Field(description="Whether there are more liked videos or not")
    user_liked_videos: list[UserVideosDataModel] = Field(
        description="The list of liked videos"
    )


class UserPinnedVideosResponseDataModel(BaseModel):
    """
    Model for the response data of pinned videos.

    Attributes:
        pinned_videos_list (list[UserVideosDataModel]): A list of data models containing information about the user's pinned videos.
    """

    pinned_videos_list: list[UserVideosDataModel] = Field(
        description="A list of video objects that match the query"
    )


class UserRepostedVideosResponseDataModel(BaseModel):
    """
    Model for the response data of reposted videos.

    Attributes:
        cursor (int): A Unix timestamp in UTC seconds indicating where to start retrieving reposted videos.
        has_more (bool): Indicates whether there are more reposted videos available for retrieval.
        reposted_videos (list[UserVideosDataModel]): A list of data models containing information about the user's reposted videos.
    """

    cursor: int = Field(
        description="Retrieve reposted videos starting from the specified Unix timestamp in UTC seconds"
    )
    has_more: bool = Field(description="Whether there are more reposted videos or not")
    reposted_videos: list[UserVideosDataModel] = Field(
        description="The list of reposted videos"
    )


class UserFollowDataModel(BaseModel):
    """
    Model for the response data of user follow.

    Attributes:
        display_name (str): The profile name of the user.
        username (str): The username of the user.
    """

    display_name: str = Field(description="The profile name of the user.")
    username: str = Field(description="The username of the user.")


class UserFollowersResponseDataModel(BaseModel):
    """
    Model for the response data of user followers.

    Attributes:
        cursor (int): A Unix timestamp in UTC seconds indicating where to start retrieving follower data.
        has_more (bool): Indicates whether there are more follower data available for retrieval.
        user_followers (list[UserFollowDataModel]): A list of data models containing information about the user's followers.
    """

    cursor: int = Field(
        description="Retrieve follower data starting from the specified Unix timestamp in UTC seconds"
    )
    has_more: bool = Field(description="Whether there are more follower data or not")
    user_followers: list[UserFollowDataModel] = Field(
        description="The list of user follower data"
    )


class UserFollowingResponseDataModel(BaseModel):
    """
    Model for the response data of user following.

    Attributes:
        cursor (int): A Unix timestamp in UTC seconds indicating where to start retrieving following data.
        has_more (bool): Indicates whether there are more following data available for retrieval.
        user_following (list[UserFollowDataModel]): A list of data models containing information about the user's following.
    """

    cursor: int = Field(
        description="Retrieve following data starting from the specified Unix timestamp in UTC seconds"
    )
    has_more: bool = Field(description="Whether there are more following data or not")
    user_following: list[UserFollowDataModel] = Field(
        description="The list of user following data"
    )


class UserLikedVideosResponseModel(BaseModel):
    """
    Model for the complete API response for liked videos.

    Attributes:
        data (UserLikedVideosDataModel): The returned list of liked video objects.
        error (ResponseErrorModel): Error information, if any.
    """

    data: UserVideosDataModel
    error: ResponseErrorModel


class UserPinnedVideosResponseModel(BaseModel):
    """
    Model for the complete API response for pinned videos.

    Attributes:
        data (UserPinnedVideosDataModel): The returned list of pinned video objects.
        error (ResponseErrorModel): Error information, if any.
    """

    data: UserPinnedVideosResponseDataModel
    error: ResponseErrorModel


class UserRepostedVideosResponseModel(BaseModel):
    """
    Model for the complete API response for reposted videos.

    Attributes:
        data (UserRepostedVideosDataModel): The returned list of reposted video objects.
        error (ResponseErrorModel): Error information, if any.
    """

    data: UserRepostedVideosResponseDataModel
    error: ResponseErrorModel


class UserFollowersResponseModel(BaseModel):
    """
    Model for the complete API response for user followers.

    Attributes:
        data (UserFollowersDataModel): The returned list of follower data.
        error (ResponseErrorModel): Error information, if any.
    """

    data: UserFollowersResponseDataModel
    error: ResponseErrorModel


class UserFollowingResponseModel(BaseModel):
    """
    Model for the complete API response for user following.

    Attributes:
        data (UserFollowingDataModel): The returned list of following data.
        error (ResponseErrorModel): Error information, if any.
    """

    data: UserFollowingResponseDataModel
    error: ResponseErrorModel

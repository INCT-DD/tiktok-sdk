"""
This module defines Pydantic models and enums for TikTok video query validation and request building.

It includes models for query conditions, operations, field names, and region codes,
as well as builder classes to construct complex TikTok video queries.
"""

from pydantic import (
    BaseModel,
    Field,
    model_validator,
    ConfigDict,
)
from enum import StrEnum
import re

from TikTok.ValidationModels.BaseModels import BaseRequestModel, ResponseErrorModel
from TikTok.ValidationModels.VideoHelper import VideoRegionCode


class VideoQueryFields(StrEnum):
    """
    Represents the possible fields for a video object.

    Attributes:
        id (str): The unique identifier for the video.
        video_description (str): The description of the video.
        create_time (str): The time the video was created.
        region_code (str): The region code associated with the video.
        share_count (str): The number of times the video has been shared.
        view_count (str): The number of times the video has been viewed.
        like_count (str): The number of likes the video has received.
        comment_count (str): The number of comments the video has received.
        music_id (str): The ID of the music used in the video.
        hashtag_names (str): The names of the hashtags associated with the video.
        username (str): The username of the video's creator.
        effect_ids (str): The IDs of the effects used in the video.
        playlist_id (str): The ID of the playlist the video belongs to.
        voice_to_text (str): The text transcription of the video's audio.
        is_stem_verified (str): Whether the video is verified as STEM content.
        favorites_count (str): The number of times the video has been added to favorites.
        video_duration (str): The duration of the video.
    """

    id = "id"
    video_description = "video_description"
    create_time = "create_time"
    region_code = "region_code"
    share_count = "share_count"
    view_count = "view_count"
    like_count = "like_count"
    comment_count = "comment_count"
    music_id = "music_id"
    hashtag_names = "hashtag_names"
    username = "username"
    effect_ids = "effect_ids"
    playlist_id = "playlist_id"
    voice_to_text = "voice_to_text"
    is_stem_verified = "is_stem_verified"
    favorites_count = "favorites_count"
    video_duration = "video_duration"


class VideoQueryOperation(StrEnum):
    """
    Enum representing the available query operations for TikTok video searches.

    Attributes:
        EQ (str): Equal to operation.
        IN (str): In operation (for multiple values).
        GT (str): Greater than operation.
        GTE (str): Greater than or equal to operation.
        LT (str): Less than operation.
        LTE (str): Less than or equal to operation.
    """

    EQ = "EQ"
    IN = "IN"
    GT = "GT"
    GTE = "GTE"
    LT = "LT"
    LTE = "LTE"


class VideoQueryFieldName(StrEnum):
    """
    Enum representing the available field names for TikTok video queries.

    Attributes:
        id (str): The unique identifier for the video.
        video_description (str): The description of the video.
        create_time (str): The time the video was created.
        region_code (str): The region code associated with the video.
        share_count (str): The number of times the video has been shared.
        view_count (str): The number of times the video has been viewed.
        like_count (str): The number of likes the video has received.
        comment_count (str): The number of comments the video has received.
        music_id (str): The ID of the music used in the video.
        hashtag_names (str): The names of the hashtags associated with the video.
        username (str): The username of the video's creator.
        effect_ids (str): The IDs of the effects used in the video.
        playlist_id (str): The ID of the playlist the video belongs to.
        voice_to_text (str): The text transcription of the video's audio.
        is_stem_verified (str): Whether the video is verified as STEM content.
        favorites_count (str): The number of times the video has been added to favorites.
        video_duration (str): The duration of the video.
    """

    id = "id"
    video_description = "video_description"
    create_time = "create_time"
    region_code = "region_code"
    share_count = "share_count"
    view_count = "view_count"
    like_count = "like_count"
    comment_count = "comment_count"
    music_id = "music_id"
    hashtag_names = "hashtag_names"
    username = "username"
    effect_ids = "effect_ids"
    playlist_id = "playlist_id"
    voice_to_text = "voice_to_text"
    is_stem_verified = "is_stem_verified"
    favorites_count = "favorites_count"
    video_duration = "video_duration"


class VideoLength(StrEnum):
    """
    Enum representing the available video length categories.

    Attributes:
        SHORT (str): Short video length category.
        MID (str): Medium video length category.
        LONG (str): Long video length category.
        EXTRA_LONG (str): Extra long video length category.
    """

    SHORT = "SHORT"
    MID = "MID"
    LONG = "LONG"
    EXTRA_LONG = "EXTRA_LONG"


class VideoCommentFields(StrEnum):
    """
    Enum representing the fields of a comment.

    Attributes:
        id (str): The unique identifier for the comment.
        video_id (str): The identifier of the video associated with the comment.
        text (str): The content of the comment.
        like_count (str): The number of likes the comment has received.
        reply_count (str): The number of replies to the comment.
        parent_comment_id (str): The identifier of the parent comment, if applicable.
        create_time (str): The timestamp when the comment was created.
    """

    id = "id"
    video_id = "video_id"
    text = "text"
    like_count = "like_count"
    reply_count = "reply_count"
    parent_comment_id = "parent_comment_id"
    create_time = "create_time"


class Condition(BaseModel):
    """
    Represents a single condition in a TikTok video query.

    Attributes:
        operation (VideoQueryOperation): The operation to apply in the condition.
        field_name (VideoQueryFieldName): The field to which the condition applies.
        field_values (list[str | int]): The values to use in the condition.
    """

    operation: VideoQueryOperation
    field_name: VideoQueryFieldName
    field_values: list[str | int]

    @model_validator(mode="after")
    @classmethod
    def validate_condition(cls, values: "Condition") -> "Condition":
        """
        Validates the condition based on the field name and its corresponding values.

        Args:
            values (Condition): The condition to validate.

        Returns:
            Condition: The validated condition.

        Raises:
            ValueError: If the condition is invalid.
        """
        field_name: VideoQueryFieldName = values.field_name
        field_values: list[str | int] = values.field_values
        match field_name:
            case VideoQueryFieldName.create_time:
                for value in field_values:
                    if not isinstance(value, str):
                        raise ValueError(
                            f"Invalid create_time type: {value}. Must be a string in YYYYMMDD format."
                        )
                    if not re.match(r"^\d{8}$", value):
                        raise ValueError(
                            f"Invalid create_time format: {value}. Use YYYYMMDD."
                        )
            case VideoQueryFieldName.username:
                for value in field_values:
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError("Username must be a non-empty string.")
            case VideoQueryFieldName.region_code:
                for value in field_values:
                    if not (
                        isinstance(value, VideoRegionCode)
                        or (
                            isinstance(value, str)
                            and value in VideoRegionCode._value2member_map_
                        )
                    ):
                        raise ValueError(
                            f"Invalid region_code: {value}. Must be a valid RegionCode."
                        )
            case VideoQueryFieldName.video_duration:
                for value in field_values:
                    if not (
                        isinstance(value, VideoLength)
                        or (
                            isinstance(value, str)
                            and value in VideoLength._value2member_map_
                        )
                    ):
                        raise ValueError(
                            f"Invalid video_duration: {value}. Must be one of {[e.value for e in VideoLength]}."
                        )
            case (
                VideoQueryFieldName.id
                | VideoQueryFieldName.music_id
                | VideoQueryFieldName.effect_ids
                | VideoQueryFieldName.playlist_id
            ):
                for value in field_values:
                    try:
                        int_value = int(value)
                        if int_value <= 0:
                            raise ValueError(
                                f"Invalid {field_name}: {value}. Must be a positive integer."
                            )
                    except (ValueError, TypeError) as err:
                        raise ValueError(
                            f"Invalid {field_name}: {value}. Must be a positive integer."
                        ) from err
            case _:
                pass
        return values


class Query(BaseModel):
    """
    Represents a complex query structure for TikTok video searches.

    Attributes:
        and_ (list[Condition] | None): List of conditions to be ANDed together.
        or_ (list[Condition] | None): List of conditions to be ORed together.
        not_ (list[Condition] | None): List of conditions to be NOTed.
    """

    model_config: ConfigDict = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )

    and_: list[Condition] | None = Field(default=None, alias="and")
    or_: list[Condition] | None = Field(default=None, alias="or")
    not_: list[Condition] | None = Field(default=None, alias="not")


class VideoQueryRequestModel(BaseRequestModel):
    """
    Represents a complete TikTok video query request.

    Attributes:
        query (Query): The complex query structure for the request.
        start_date (str): The lower bound of video creation time in YYYYMMDD format.
        end_date (str): The upper bound of video creation time in YYYYMMDD format.
        max_count (int | None): The maximum number of videos to return.
        cursor (int | None): The index to start retrieving video results from.
        search_id (str | None): The unique identifier for a cached search result.
        is_random (bool): Flag indicating whether to return results in random order.
    """

    model_config: ConfigDict = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )

    query: Query = Field(
        ...,
        description="""
        A JSON object that contains three types of children: and, or, and not, each of which is a list of conditions. 
        An valid query must contain at least one non-empty and, or or not condition lists
        """,
    )
    start_date: str = Field(
        ...,
        description="The lower bound of video creation time in YYYYMMDD format. Must be before end_date.",
        pattern=r"^\d{8}$",
    )
    end_date: str = Field(
        ...,
        description="""
        The upper bound of video creation time in YYYYMMDD format. Must be after start_date. 
        The end_date must be no more than 30 days after the start_date
        """,
        pattern=r"^\d{8}$",
    )
    max_count: int | None = Field(
        default=None,
        gt=0,
        le=100,
        description="""
        The number of videos in response. Default is 20, max is 100. 
        It is possible that the API returns less videos than the max count due to reasons such as videos deleted/marked as private by users etc.
        """,
    )
    cursor: int | None = Field(
        default=None,
        description="Retrieve video results starting from the specified index",
    )
    search_id: str | None = Field(
        default=None,
        description="""
        The unique identifier assigned to a cached search result.
        This identifier enables the resumption of a prior search and retrieval of additional results based on the same search criteria.
        """,
    )
    is_random: bool = Field(
        default=False,
        description="""The flag that indicates whether to return results in a random order.
If set to true, then the API returns 1 - 100 videos in random order that matches the query.
If set to false or not set with any value, then the API returns results in the decreasing order of video IDs.""",
    )


class QueryBuilder:
    """
    A builder class for constructing complex TikTok video queries.

    This class provides methods to add AND, OR, and NOT conditions to the query.
    """

    def __init__(self):
        """Initialize the QueryBuilder with empty condition lists."""
        self.and_conditions = []
        self.or_conditions = []
        self.not_conditions = []

    def and_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> "QueryBuilder":
        """
        Add an AND condition to the query.

        Args:
            operation (VideoQueryOperation): The operation for the condition.
            field_name (VideoQueryFieldName): The field name for the condition.
            field_values (list[str | int]): The values for the condition.

        Returns:
            QueryBuilder: The current QueryBuilder instance for method chaining.
        """
        field_values = [
            value.value if isinstance(value, StrEnum) else value
            for value in field_values
        ]
        condition = Condition(
            operation=operation, field_name=field_name, field_values=field_values
        )
        self.and_conditions.append(condition)
        return self

    def or_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> "QueryBuilder":
        """
        Add an OR condition to the query.

        Args:
            operation (VideoQueryOperation): The operation for the condition.
            field_name (VideoQueryFieldName): The field name for the condition.
            field_values (list[str | int]): The values for the condition.

        Returns:
            QueryBuilder: The current QueryBuilder instance for method chaining.
        """
        field_values = [
            value.value if isinstance(value, StrEnum) else value
            for value in field_values
        ]
        condition = Condition(
            operation=operation, field_name=field_name, field_values=field_values
        )
        self.or_conditions.append(condition)
        return self

    def not_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> "QueryBuilder":
        """
        Add a NOT condition to the query.

        Args:
            operation (VideoQueryOperation): The operation for the condition.
            field_name (VideoQueryFieldName): The field name for the condition.
            field_values (list[str | int]): The values for the condition.

        Returns:
            QueryBuilder: The current QueryBuilder instance for method chaining.
        """
        field_values = [
            value.value if isinstance(value, StrEnum) else value
            for value in field_values
        ]
        condition = Condition(
            operation=operation, field_name=field_name, field_values=field_values
        )
        self.not_conditions.append(condition)
        return self

    def build(self) -> Query:
        """
        Build and return the final Query object.

        Returns:
            Query: The constructed Query object.
        """
        return Query(
            and_=self.and_conditions if self.and_conditions else None,
            or_=self.or_conditions if self.or_conditions else None,
            not_=self.not_conditions if self.not_conditions else None,
        )


class VideoQueryRequestBuilder:
    """
    A builder class for constructing TikTokQueryRequest objects.

    This class provides methods to set various parameters of the TikTokQueryRequest
    and to add query conditions using the QueryBuilder.
    """

    def __init__(self):
        """Initialize the TikTokQueryRequestBuilder with default values."""
        self.query_builder = QueryBuilder()
        self._start_date: str | None = None
        self._end_date: str | None = None
        self._max_count: int | None = None
        self._cursor: int | None = None
        self._search_id: str | None = None
        self._is_random: bool = False

    def start_date(self, start_date: str) -> "VideoQueryRequestBuilder":
        """
        Set the start date for the query.

        Args:
            start_date (str): The start date in YYYYMMDD format.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self._start_date = start_date
        return self

    def end_date(self, end_date: str) -> "VideoQueryRequestBuilder":
        """
        Set the end date for the query.

        Args:
            end_date (str): The end date in YYYYMMDD format.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self._end_date = end_date
        return self

    def max_count(self, max_count: int) -> "VideoQueryRequestBuilder":
        """
        Set the maximum number of results to return.

        Args:
            max_count (int): The maximum number of results.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self._max_count = max_count
        return self

    def cursor(self, cursor: int) -> "VideoQueryRequestBuilder":
        """
        Set the cursor position for pagination.

        Args:
            cursor (int): The cursor position.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self._cursor = cursor
        return self

    def search_id(self, search_id: str) -> "VideoQueryRequestBuilder":
        """
        Set the search ID for a cached search result.

        Args:
            search_id (str): The search ID.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self._search_id = search_id
        return self

    def is_random(self, is_random: bool) -> "VideoQueryRequestBuilder":
        """
        Set whether the results should be returned in random order.

        Args:
            is_random (bool): True if results should be randomized, False otherwise.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self._is_random = is_random
        return self

    def and_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> "VideoQueryRequestBuilder":
        """
        Add an AND condition to the query.

        Args:
            operation (VideoQueryOperation): The operation for the condition.
            field_name (VideoQueryFieldName): The field name for the condition.
            field_values (list[str | int]): The values for the condition.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self.query_builder.and_(operation, field_name, field_values)
        return self

    def or_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> "VideoQueryRequestBuilder":
        """
        Add an OR condition to the query.

        Args:
            operation (VideoQueryOperation): The operation for the condition.
            field_name (VideoQueryFieldName): The field name for the condition.
            field_values (list[str | int]): The values for the condition.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self.query_builder.or_(operation, field_name, field_values)
        return self

    def not_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> "VideoQueryRequestBuilder":
        """
        Add a NOT condition to the query.

        Args:
            operation (VideoQueryOperation): The operation for the condition.
            field_name (VideoQueryFieldName): The field name for the condition.
            field_values (list[str | int]): The values for the condition.

        Returns:
            TikTokQueryRequestBuilder: The current builder instance for method chaining.
        """
        self.query_builder.not_(operation, field_name, field_values)
        return self

    def build(self) -> VideoQueryRequestModel:
        """
        Build and return the final TikTokQueryRequest object.

        Returns:
            TikTokQueryRequest: The constructed TikTokQueryRequest object.
        """
        query = self.query_builder.build()
        return VideoQueryRequestModel(
            query=query,
            start_date=self._start_date,
            end_date=self._end_date,
            max_count=self._max_count,
            cursor=self._cursor,
            search_id=self._search_id,
            is_random=self._is_random,
        )


class VideoDataModel(BaseModel):
    """
    Model representing the fields of a TikTok video search query.

    Each field provides metadata about a TikTok video, including identifiers, engagement metrics,
    and descriptive elements such as hashtags and effects used in the video.

    Attributes:
        id (int): Unique identifier for the TikTok video. Also called 'item_id' or 'video_id'.
        create_time (int): UTC Unix epoch (in seconds) of when the TikTok video was posted.
        username (str): The video's author's username.
        region_code (str): A two-digit code for the country where the video creator registered their account.
        video_description (str): The description of the video, also known as the title.
        music_id (int): The music_id used in the video.
        like_count (int): The number of likes the video has received.
        comment_count (int): The number of comments the video has received.
        share_count (int): The number of shares the video has received.
        view_count (int): The number of video views the video has received.
        effect_ids (list[str]): The list of effect ids applied on the video.
        hashtag_names (list[str]): The list of hashtag names that the video participates in.
        playlist_id (int): The ID of the playlist that the video belongs to.
        voice_to_text (str): Voice to text and subtitles (for videos that have voice-to-text features on).
        is_stem_verified (bool): Whether the video has been verified as being high-quality STEM content.
        video_duration (int): The duration of the video, in seconds.
        favourites_count (int): The number of favorites that a video receives.
    """

    id: int | None = Field(
        default=None,
        description="Unique identifier for the TikTok video. Also called 'item_id' or 'video_id'",
    )
    create_time: int | None = Field(
        default=None,
        description="UTC Unix epoch (in seconds) of when the TikTok video was posted. (Inherited field from TNS research API)",
    )
    username: str | None = Field(
        default=None, description="The video's author's username"
    )
    region_code: str | None = Field(
        default=None,
        description="A two-digit code for the country where the video creator registered their account",
    )
    video_description: str | None = Field(
        default=None,
        description="The description of the video, also known as the title",
    )
    music_id: int | None = Field(
        default=None, description="The music_id used in the video"
    )
    like_count: int | None = Field(
        default=None, description="The number of likes the video has received"
    )
    comment_count: int | None = Field(
        default=None, description="The number of comments the video has received"
    )
    share_count: int | None = Field(
        default=None, description="The number of shares the video has received"
    )
    view_count: int | None = Field(
        default=None, description="The number of video views the video has received"
    )
    effect_ids: list[str] | None = Field(
        default=None, description="The list of effect ids applied on the video"
    )
    hashtag_names: list[str] | None = Field(
        default=None,
        description="The list of hashtag names that the video participates in",
    )
    playlist_id: int | None = Field(
        default=None, description="The ID of the playlist that the video belongs to"
    )
    voice_to_text: str | None = Field(
        default=None,
        description="Voice to text and subtitles (for videos that have voice-to-text features on, show the texts already generated)",
    )
    is_stem_verified: bool | None = Field(
        default=None,
        description="Whether the video has been verified as being high-quality STEM content",
    )
    video_duration: int | None = Field(
        default=None, description="The duration of the video, in seconds"
    )
    favourites_count: int | None = Field(
        default=None, description="The number of favorites that a video receives"
    )


class VideoSearchQueryDataModel(BaseModel):
    """
    Model representing the data of a TikTok video search query.

    Attributes:
        videos (list[VideoDataModel]): List of video data models matching the search query.
        cursor (int): The cursor position for pagination.
        has_more (bool): Indicates if there are more results available.
        search_id (str): The unique identifier for the search query.
    """

    videos: list[VideoDataModel]
    cursor: int
    has_more: bool
    search_id: str


class VideoQueryResponseModel(BaseModel):
    """
    Model representing the complete API response for a TikTok video search query.

    Attributes:
        data (VideoSearchQueryDataModel): The data containing the search results.
        error (ResponseErrorModel): Error information, if any.
    """

    data: VideoSearchQueryDataModel
    error: ResponseErrorModel


class VideoCommentRequestModel(BaseRequestModel):
    video_id: int = Field(
        ..., description="The ID of the video to retrieve comments for"
    )
    max_count: int | None = Field(
        default=None,
        gt=0,
        le=100,
        description="The maximum number of comments to return. Default is 20, max is 100",
    )
    cursor: int | None = Field(
        default=None, description="Retrieve comments starting from the specified index"
    )


class VideoCommentModel(BaseModel):
    """
    Model representing a TikTok video comment.

    Attributes:
        id (int): The unique identifier for the comment.
        text (str): The content of the comment.
        video_id (int): The identifier of the video associated with the comment.
        parent_comment_id (int): The identifier of the parent comment, if the comment is a reply.
        like_count (int): The number of likes the comment has received.
        reply_count (int): The number of replies to the comment.
        create_time (int): The UTC Unix epoch (in seconds) of when the comment was posted.
    """

    id: int | None = Field(
        default=None, description="The unique identifier for the comment"
    )
    text: str | None = Field(default=None, description="The content of the comment")
    video_id: int | None = Field(
        default=None,
        description="The identifier of the video associated with the comment",
    )
    parent_comment_id: int | None = Field(
        default=None,
        description="The identifier of the parent comment, if the comment is a reply",
    )
    like_count: int | None = Field(
        default=None, description="The number of likes the comment has received"
    )
    reply_count: int | None = Field(
        default=None, description="The number of replies to the comment"
    )
    create_time: int | None = Field(
        default=None,
        description="The UTC Unix epoch (in seconds) of when the comment was posted",
    )


class VideoCommentResponseDataModel(BaseModel):
    """
    Model representing the data of a TikTok video comment response.

    Attributes:
        comments (list[VideoCommentModel]): List of video comment models.
        cursor (int): The cursor position for pagination.
        has_more (bool): Indicates if there are more results available.
    """

    comments: list[VideoCommentModel]
    cursor: int
    has_more: bool


class VideoCommentResponseModel(BaseModel):
    """
    Model representing the complete API response for a TikTok video comment query.

    Attributes:
        data (VideoCommentResponseDataModel): The data containing the comment results.
        error (ResponseErrorModel): Error information, if any.
    """

    data: VideoCommentResponseDataModel
    error: ResponseErrorModel

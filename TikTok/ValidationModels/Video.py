"""Build video searches and read video, comment, and reply results."""

import re
from datetime import date
from enum import StrEnum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    StrictStr,
    field_serializer,
    model_validator,
)

from TikTok.ValidationModels.BaseModels import BaseRequestModel, ResponseErrorModel
from TikTok.ValidationModels.VideoHelper import VideoRecord, VideoRegionCode


class VideoQueryFields(StrEnum):
    """Select the fields that TikTok returns for each video in a search.

    create_time is a Unix timestamp in seconds. video_duration is the
    duration in seconds. region_code identifies the country where the
    creator registered. Use the info lists for hashtag, sticker, and
    effect details. video_mention_list contains the tagged usernames.
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
    hashtag_info_list = "hashtag_info_list"
    sticker_info_list = "sticker_info_list"
    effect_info_list = "effect_info_list"
    video_mention_list = "video_mention_list"
    video_label = "video_label"
    video_tag = "video_tag"


class VideoQueryOperation(StrEnum):
    """Select the comparison for a video condition.

    EQ compares one value. IN matches any of the given values. GT and LT
    apply strict bounds. GTE and LTE include the bound.
    """

    EQ = "EQ"
    IN = "IN"
    GT = "GT"
    GTE = "GTE"
    LT = "LT"
    LTE = "LTE"


class VideoQueryFieldName(StrEnum):
    """Select a field for a video search condition.

    Use create_date for a UTC date, video_length for a duration category, and
    keyword for text in the description. TikTok applies approximate text matching.
    The older Python names id, create_time, effect_ids, and video_duration send
    the corresponding filter names shown below.
    """

    create_date = "create_date"
    username = "username"
    region_code = "region_code"
    video_id = "video_id"
    hashtag_name = "hashtag_name"
    keyword = "keyword"
    music_id = "music_id"
    effect_id = "effect_id"
    video_length = "video_length"
    view_count = "view_count"
    comment_count = "comment_count"

    id = video_id
    create_time = create_date
    effect_ids = effect_id
    video_duration = video_length


class VideoLength(StrEnum):
    """Select a duration category for the video_length condition."""

    SHORT = "SHORT"
    MID = "MID"
    LONG = "LONG"
    EXTRA_LONG = "EXTRA_LONG"


class VideoCommentFields(StrEnum):
    """Select the fields that TikTok returns for each comment or reply."""

    id = "id"
    video_id = "video_id"
    text = "text"
    like_count = "like_count"
    reply_count = "reply_count"
    parent_comment_id = "parent_comment_id"
    create_time = "create_time"
    display_name = "display_name"


def _query_date(value: str) -> date:
    """Return the calendar date of a YYYYMMDD string.

    Raise ValueError if the input has a different format or an invalid date.
    """
    if not re.fullmatch(r"[0-9]{8}", value):
        raise ValueError(f"Expected a date in YYYYMMDD format, got {value!r}")
    return date.fromisoformat(value)


class Condition(BaseModel):
    """Compare a search field with the supplied values.

    Use IN for one or more values. Every other operator takes one value.
    GT, GTE, LT, and LTE apply to create_date, view_count, and comment_count.
    The SDK sends all operands as JSON strings. It accepts integer IDs and
    counts as a convenience.
    """

    model_config = ConfigDict(extra="forbid")

    operation: VideoQueryOperation
    field_name: VideoQueryFieldName
    field_values: list[StrictStr | StrictInt] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_condition(self) -> Condition:
        """Validate the operands and return the condition.

        Raise ValueError for an invalid operation, number of operands, date,
        region code, duration category, numeric operand, or empty text.
        """
        if self.operation != VideoQueryOperation.IN and len(self.field_values) != 1:
            raise ValueError(f"{self.operation} requires exactly one field value")
        if self.operation not in (
            VideoQueryOperation.EQ,
            VideoQueryOperation.IN,
        ) and self.field_name not in (
            VideoQueryFieldName.create_date,
            VideoQueryFieldName.view_count,
            VideoQueryFieldName.comment_count,
        ):
            raise ValueError(
                f"{self.operation} applies only to create_date, view_count, or comment_count"
            )
        for value in self.field_values:
            match self.field_name:
                case VideoQueryFieldName.create_date:
                    _query_date(str(value))
                case VideoQueryFieldName.region_code:
                    VideoRegionCode(value)
                case VideoQueryFieldName.video_length:
                    VideoLength(value)
                case (
                    VideoQueryFieldName.video_id
                    | VideoQueryFieldName.music_id
                    | VideoQueryFieldName.effect_id
                ):
                    if not re.fullmatch(r"[0-9]+", str(value)):
                        raise ValueError(f"{self.field_name} requires a decimal ID")
                case VideoQueryFieldName.view_count | VideoQueryFieldName.comment_count:
                    if not re.fullmatch(r"-?[0-9]+", str(value)):
                        raise ValueError(f"{self.field_name} requires an integer")
                case _:
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(f"{self.field_name} requires nonempty text")
        return self

    @field_serializer("field_values")
    def serialize_values(self, values: list[str | int]) -> list[str]:
        """Return every operand as a string for the Research API."""
        return [str(value) for value in values]


class Query(BaseModel):
    """Group the conditions for a video search.

    A result must match every condition in and, at least one condition in
    or when present, and none of the conditions in not. Supply a nonempty
    list for at least one group.
    """

    model_config = ConfigDict(validate_by_name=True, extra="forbid")

    and_: list[Condition] | None = Field(default=None, alias="and")
    or_: list[Condition] | None = Field(default=None, alias="or")
    not_: list[Condition] | None = Field(default=None, alias="not")

    @model_validator(mode="after")
    def require_conditions(self) -> Query:
        """Return the query or raise ValueError if every group is empty."""
        if not any((self.and_, self.or_, self.not_)):
            raise ValueError("Supply at least one condition in and, or, or not")
        return self


class VideoQueryRequestModel(BaseRequestModel):
    """Search for videos in an inclusive range of UTC calendar dates.

    Supply at least one condition and two dates in YYYYMMDD format. The end
    date can be the start date or up to 30 days later. Request up to 100
    videos per page. To continue a search, use its cursor and search_id
    with the same conditions and dates. Set is_random to sample results.
    """

    query: Query
    start_date: str = Field(description="First UTC date in YYYYMMDD format.")
    end_date: str = Field(description="Last UTC date in YYYYMMDD format.")
    max_count: int | None = Field(
        default=None, gt=0, le=100, description="Maximum videos per page."
    )
    cursor: int | None = Field(
        default=None, ge=0, description="Starting index in the search results."
    )
    search_id: str | None = Field(
        default=None, description="ID of the cached search to continue."
    )
    is_random: bool = Field(
        default=False,
        description="Return matches in random order. The default is descending video ID.",
    )

    @model_validator(mode="after")
    def validate_dates(self) -> VideoQueryRequestModel:
        """Return the request or raise ValueError for invalid dates or bounds."""
        span = (_query_date(self.end_date) - _query_date(self.start_date)).days
        if not 0 <= span <= 30:
            raise ValueError("end_date must be from 0 to 30 days after start_date")
        return self


class QueryBuilder:
    """Build the three condition groups for a video search."""

    def __init__(self) -> None:
        """Start with an empty list for each condition group."""
        self.and_conditions: list[Condition] = []
        self.or_conditions: list[Condition] = []
        self.not_conditions: list[Condition] = []

    def and_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> QueryBuilder:
        """Require the comparison to match and return the builder.

        Supply the operator, filter field, and operands. An invalid
        comparison raises a validation error.
        """
        self.and_conditions.append(
            Condition(
                operation=operation, field_name=field_name, field_values=field_values
            )
        )
        return self

    def or_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> QueryBuilder:
        """Add an alternative comparison and return the builder.

        At least one comparison in this group must match. An invalid
        operator, field, or operand raises a validation error.
        """
        self.or_conditions.append(
            Condition(
                operation=operation, field_name=field_name, field_values=field_values
            )
        )
        return self

    def not_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> QueryBuilder:
        """Exclude matches for the comparison and return the builder.

        Each comparison in this group excludes matching videos. An invalid
        operator, field, or operand raises a validation error.
        """
        self.not_conditions.append(
            Condition(
                operation=operation, field_name=field_name, field_values=field_values
            )
        )
        return self

    def build(self) -> Query:
        """Return the query or raise a validation error if it has no conditions."""
        return Query(
            and_=self.and_conditions or None,
            or_=self.or_conditions or None,
            not_=self.not_conditions or None,
        )


class VideoQueryRequestBuilder:
    """Build a search request with its dates, conditions, and page options.

    Call start_date and end_date, add at least one condition, then call build.
    The returned model can be passed to query.video.search.
    """

    def __init__(self) -> None:
        """Start with no dates or conditions, and use the API page size."""
        self.query_builder = QueryBuilder()
        self._start_date: str | None = None
        self._end_date: str | None = None
        self._max_count: int | None = None
        self._cursor: int | None = None
        self._search_id: str | None = None
        self._is_random = False

    def start_date(self, start_date: str) -> VideoQueryRequestBuilder:
        """Set the first UTC date in YYYYMMDD format and return the builder."""
        self._start_date = start_date
        return self

    def end_date(self, end_date: str) -> VideoQueryRequestBuilder:
        """Set the last UTC date in YYYYMMDD format and return the builder."""
        self._end_date = end_date
        return self

    def max_count(self, max_count: int) -> VideoQueryRequestBuilder:
        """Set the page size from 1 through 100 and return the builder."""
        self._max_count = max_count
        return self

    def cursor(self, cursor: int) -> VideoQueryRequestBuilder:
        """Set the index for the next page and return the builder."""
        self._cursor = cursor
        return self

    def search_id(self, search_id: str) -> VideoQueryRequestBuilder:
        """Set the ID of the search to continue and return the builder."""
        self._search_id = search_id
        return self

    def is_random(self, is_random: bool) -> VideoQueryRequestBuilder:
        """Set whether TikTok returns videos in random order and return the builder."""
        self._is_random = is_random
        return self

    def and_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> VideoQueryRequestBuilder:
        """Require the given field comparison and return the request builder."""
        self.query_builder.and_(operation, field_name, field_values)
        return self

    def or_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> VideoQueryRequestBuilder:
        """Add an alternative field comparison and return the request builder."""
        self.query_builder.or_(operation, field_name, field_values)
        return self

    def not_(
        self,
        operation: VideoQueryOperation,
        field_name: VideoQueryFieldName,
        field_values: list[str | int],
    ) -> VideoQueryRequestBuilder:
        """Exclude matches for the given comparison and return the request builder."""
        self.query_builder.not_(operation, field_name, field_values)
        return self

    def build(self) -> VideoQueryRequestModel:
        """Return a request with the current conditions, dates, and page options.

        Raise a validation error if the query is empty or the dates or page
        options are invalid.
        """
        return VideoQueryRequestModel.model_validate(
            {
                "query": self.query_builder.build(),
                "start_date": self._start_date,
                "end_date": self._end_date,
                "max_count": self._max_count,
                "cursor": self._cursor,
                "search_id": self._search_id,
                "is_random": self._is_random,
            }
        )


class VideoDataModel(VideoRecord):
    """Read the selected fields of a video search result.

    Search can also return the effect IDs, playlist ID, and transcript.
    An omitted field has the value None.
    """

    effect_ids: list[str] | None = Field(
        default=None, description="Effect IDs on the video."
    )
    playlist_id: int | None = Field(
        default=None, description="ID of the video's playlist."
    )
    voice_to_text: str | None = Field(
        default=None, description="Transcript or subtitle text."
    )


class VideoSearchQueryDataModel(BaseModel):
    """Read a page of videos and the information to continue the search.

    The API can omit the cursor on the last page. Use has_more to determine
    if another page is available.
    """

    videos: list[VideoDataModel]
    cursor: int | None = None
    has_more: bool
    search_id: str


class VideoQueryResponseModel(BaseModel):
    """Read the video search result and TikTok's request status."""

    data: VideoSearchQueryDataModel
    error: ResponseErrorModel


class VideoCommentRequestModel(BaseRequestModel):
    """Request comments for one video or replies to one comment.

    Supply exactly one ID. Use the returned cursor to request another page.
    TikTok supplies a default page size of 10 and accepts up to 100.
    """

    video_id: int | None = None
    comment_id: int | None = None
    max_count: int | None = Field(default=None, gt=0, le=100)
    cursor: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def require_one_id(self) -> VideoCommentRequestModel:
        """Return the request or raise ValueError unless it selects one ID."""
        if (self.video_id is None) == (self.comment_id is None):
            raise ValueError("Supply exactly one of video_id and comment_id")
        return self


class VideoCommentModel(BaseModel):
    """Read the selected fields for a comment or reply.

    create_time is a Unix timestamp in seconds. display_name identifies the
    author by their display name. An omitted field has the value None.
    """

    id: int | None = None
    text: str | None = None
    video_id: int | None = None
    parent_comment_id: int | None = None
    like_count: int | None = None
    reply_count: int | None = None
    create_time: int | None = None
    display_name: str | None = None


class VideoCommentResponseDataModel(BaseModel):
    """Read a page of comments or replies and its pagination data.

    TikTok can return an empty data object when the selected item is
    unavailable. This gives an empty final page with no cursor.
    """

    comments: list[VideoCommentModel]
    cursor: int | None = None
    has_more: bool

    @model_validator(mode="before")
    @classmethod
    def read_empty_page(cls, data: object) -> object:
        """Supply the final page values when TikTok returns an empty object."""
        if data == {}:
            return {"comments": [], "has_more": False}
        return data

    @model_validator(mode="after")
    def require_next_cursor(self) -> VideoCommentResponseDataModel:
        """Raise ValueError if another page is available but its cursor is absent."""
        if self.has_more and self.cursor is None:
            raise ValueError("A comment page with has_more requires a cursor")
        return self


class VideoCommentResponseModel(BaseModel):
    """Read the comment or reply results and TikTok's request status.

    A successful response for an unavailable item can omit data. Its result
    is an empty final page.
    """

    data: VideoCommentResponseDataModel
    error: ResponseErrorModel

    @model_validator(mode="before")
    @classmethod
    def read_missing_page(cls, response: object) -> object:
        """Supply an empty page if a successful response omits data."""
        match response:
            case {"error": {"code": "ok"}} if "data" not in response:
                return {**response, "data": {}}
        return response

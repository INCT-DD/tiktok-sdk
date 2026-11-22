"""Validate search conditions, groups, and date limits for video requests."""

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

from TikTok.ValidationModels.BaseModels import BaseRequestModel
from TikTok.ValidationModels.VideoHelper import VideoRegionCode


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
            self._validate_operand(value)
        return self

    def _validate_operand(self, value: str | int) -> None:
        """Raise ValueError if the field cannot accept this operand."""
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

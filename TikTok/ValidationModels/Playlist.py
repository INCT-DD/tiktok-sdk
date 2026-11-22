"""
Defines data models for handling playlist-related API requests and responses in the TikTok API.
"""

from enum import StrEnum

from pydantic import BaseModel, Field

from TikTok.ValidationModels.BaseModels import BaseRequestModel, ResponseErrorModel


class PlaylistInfoQueryFields(StrEnum):
    """Select playlist metadata. Pagination details accompany each page."""

    playlist_id = "playlist_id"
    playlist_item_total = "playlist_item_total"
    playlist_last_updated = "playlist_last_updated"
    playlist_name = "playlist_name"
    playlist_video_ids = "playlist_video_ids"


class InfoRequestModel(BaseRequestModel):
    """
    Model for the playlist info request.

    Attributes:
        playlist_id (int): The unique ID of the playlist.
        cursor (int | None): The index to start retrieving video results from.
        max_count (int | None): The maximum number of videos to return in the page.
    """

    playlist_id: int = Field(description="The unique ID of the playlist.")
    cursor: int | None = Field(
        default=None,
        description="Retrieve video results starting from the specified index",
    )
    max_count: int | None = Field(
        default=None,
        gt=0,
        description="Maximum number of videos to return in this page.",
    )


class ResponseDataModel(BaseModel):
    """
    Store the selected playlist fields and the pagination details.

    The API can omit metadata when the playlist has no accessible data or
    the caller requested a subset of fields. Use ``has_more`` and ``cursor``
    to get the next page.
    """

    playlist_id: int | None = Field(
        default=None, description="The unique ID of the playlist"
    )
    playlist_item_total: int | None = Field(
        default=None, description="Total number of items in the playlist."
    )
    playlist_last_updated: int | None = Field(
        default=None, description="Time of the last playlist update."
    )
    playlist_name: str | None = Field(default=None, description="Name of the playlist.")
    playlist_video_ids: list[int] | None = Field(
        default=None, description="Video IDs returned in this page."
    )
    cursor: int = Field(description="The cursor position for pagination.")
    has_more: bool = Field(
        description="Indicates whether there are more videos in the playlist."
    )


class InfoResponseModel(BaseModel):
    """
    Model for the complete API response for playlist information.

    Attributes:
        data (ResponseDataModel): Playlist data.
        error (ResponseErrorModel): Error information, if any.
    """

    data: ResponseDataModel
    error: ResponseErrorModel

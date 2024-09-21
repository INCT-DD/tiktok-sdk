"""
Defines data models for handling playlist-related API requests and responses in the TikTok API.
"""

from pydantic import BaseModel, Field

from TikTok.ValidationModels.BaseModels import BaseRequestModel, ResponseErrorModel


class InfoRequestModel(BaseRequestModel):
    """
    Model for the playlist info request.

    Attributes:
        playlist_id (int): The unique ID of the playlist.
        cursor (int | None): The index to start retrieving video results from.
    """

    playlist_id: int = Field(description="The unique ID of the playlist.")
    cursor: int | None = Field(
        default=None,
        description="Retrieve video results starting from the specified index",
    )


class ResponseDataModel(BaseRequestModel):
    """
    Model for playlist data in the API response.

    Attributes:
        playlist_id (int): The unique ID of the playlist.
        playlist_item_total (int): The total number of items in the playlist.
        playlist_last_updated (int): Timestamp of when the playlist was last updated.
        playlist_name (str): The name of the playlist.
        playlist_video_ids (list[int]): A list of all video IDs in the playlist.
    """

    playlist_id: int = Field(description="The unique ID of the playlist")
    playlist_item_total: int = Field(
        description="Provides the total number of items in a playlist"
    )
    playlist_last_updated: int = Field(
        description="Provides info on when the playlist was last updated"
    )
    playlist_name: str = Field(description="The name of the playlist")
    playlist_video_ids: list[int] = Field(
        description="Provides a list of all video IDs in a playlist."
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

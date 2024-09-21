"""
This module contains the PlaylistQueries class for handling playlist-related API queries to the TikTok platform.
"""

from TikTok.ValidationModels import Playlist
from TikTok.Queries.Common import QueryClass


class PlaylistQueries(QueryClass):
    async def info(
        self, playlist_id: int, cursor: int | None = None
    ) -> Playlist.ResponseDataModel:
        """
        This method sends a request to the TikTok API to retrieve playlist information based on the provided playlist ID.

        Parameters:
            playlist_id (int): The ID of the TikTok playlist.
            cursor (int | None): An optional cursor for pagination.

        Returns:
            Playlist.ResponseDataModel: The response data model containing playlist information.

        Raises:
            QueryException: If the API query fails or returns an error.
            ValidationError: If the response body is invalid according to the expected model.
            Exception: For any other unexpected errors that may occur during the API request.
        """
        return await self._fetch_data(
            url=self.query.endpoints.PlaylistInfoURL,
            request_model_class=Playlist.InfoRequestModel,
            response_model_class=Playlist.InfoResponseModel,
            json_data={"playlist_id": playlist_id, "cursor": cursor},
        )

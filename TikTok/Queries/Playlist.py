"""Query public playlists through the Research API."""

from TikTok.Queries.Common import QueryClass
from TikTok.ValidationModels import Playlist


class PlaylistQueries(QueryClass):
    """Get playlist fields and pages of video IDs."""

    async def info(
        self,
        playlist_id: int,
        cursor: int | None = None,
        *,
        max_count: int | None = None,
        fields: list[Playlist.PlaylistInfoQueryFields] | None = None,
    ) -> Playlist.InfoResponseModel:
        """Get one page of a public playlist.

        Give the playlist ID. To continue, pass the previous page's cursor.
        Set max_count to a positive number to limit the page size. An optional
        fields selection is sent in the URL. TikTok can return additional
        metadata. Omit fields to use the endpoint default.

        The response contains the selected metadata, pagination details, and
        the TikTok request log ID. Invalid fields or counts raise ValueError.
        An API or transport failure raises QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.PlaylistInfoURL,
            response_model_class=Playlist.InfoResponseModel,
            params=(
                self._build_params(fields, Playlist.PlaylistInfoQueryFields)
                if fields is not None
                else None
            ),
            request=Playlist.InfoRequestModel(
                playlist_id=playlist_id, cursor=cursor, max_count=max_count
            ),
        )

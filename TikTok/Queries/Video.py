"""Query videos, video comments, and comment replies with the Research API."""

from collections.abc import Sequence

from TikTok.Queries.Common import QueryClass
from TikTok.ValidationModels import Video


class VideoQueries(QueryClass):
    """Send video search and comment requests with a Research API client."""

    async def search(
        self,
        request: Video.VideoQueryRequestModel,
        fields: Sequence[Video.VideoQueryFields],
    ) -> Video.VideoQueryResponseModel:
        """Return one page of videos that match the search request.

        Select at least one video field. When the response has more videos,
        send its cursor and search_id with the original query and dates.
        Invalid fields raise ValueError. API errors raise QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.VideoSearchURL,
            request_model_class=Video.VideoQueryRequestModel,
            response_model_class=Video.VideoQueryResponseModel,
            params=self._build_params(fields, Video.VideoQueryFields),
            json_data=request.model_dump(by_alias=True, exclude_none=True),
        )

    async def comments(
        self,
        video_id: int,
        fields: list[Video.VideoCommentFields],
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> Video.VideoCommentResponseModel:
        """
        Retrieves comments for a specific video.

        Parameters:
            video_id (int): The ID of the video for which to retrieve comments.
            fields (list[Video.VideoCommentFields]): A list of fields to include in the response.
            max_count (int | None): The maximum number of comments to retrieve. Defaults to None.
            cursor (int | None): The cursor for pagination. Defaults to None.

        Returns:
            Video.VideoCommentResponseModel: The response model containing the video comments.
        """
        return await self._fetch_data(
            url=self.query.endpoints.VideoCommentsURL,
            request_model_class=Video.VideoCommentRequestModel,
            response_model_class=Video.VideoCommentResponseModel,
            params=self._build_params(fields, Video.VideoCommentFields),
            json_data={
                "video_id": video_id,
                "max_count": max_count,
                "cursor": cursor,
            },
        )

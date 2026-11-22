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
        video_id: int | None = None,
        fields: Sequence[Video.VideoCommentFields] = (),
        max_count: int | None = None,
        cursor: int | None = None,
        *,
        comment_id: int | None = None,
    ) -> Video.VideoCommentResponseModel:
        """Return one page of comments on a video or replies to a comment.

        Supply exactly one of video_id and comment_id. Select at least one
        comment field. Use max_count to request up to 100 items and cursor
        to continue from an earlier page.

        Invalid selectors, IDs, or page options raise ValueError. API errors
        raise QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.VideoCommentsURL,
            request_model_class=Video.VideoCommentRequestModel,
            response_model_class=Video.VideoCommentResponseModel,
            params=self._build_params(fields, Video.VideoCommentFields),
            json_data={
                "video_id": video_id,
                "comment_id": comment_id,
                "max_count": max_count,
                "cursor": cursor,
            },
        )

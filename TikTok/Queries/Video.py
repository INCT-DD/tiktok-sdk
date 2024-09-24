"""
This module contains the VideoQueries class for handling video-related API queries to the TikTok platform.
"""

from TikTok.ValidationModels import Video

from TikTok.Queries.Common import QueryClass, RequestModel, ResponseModel


class VideoQueries(QueryClass[RequestModel, ResponseModel]):
    """
    A class to handle video-related API queries to the TikTok platform.

    This class inherits from QueryClass and provides methods to interact with the TikTok API
    for retrieving video information.
    """

    async def search(
        self,
        request: Video.VideoQueryRequestModel,
        fields: list[Video.VideoQueryFields],
    ) -> Video.VideoQueryResponseModel:
        """
        Searches for videos based on the provided request parameters.

        Parameters:
            request (Video.VideoQueryRequestModel): The request parameters for the video search.
            fields (list[Video.VideoQueryFields]): A list of fields to include in the response.

        Returns:
            Video.VideoQueryResponseModel: The response model containing the video search results.
        """
        return await self._fetch_data(
            url=self.query.endpoints.VideoSearchURL,
            request_model_class=Video.VideoQueryRequestModel,
            response_model_class=Video.VideoQueryResponseModel,
            params=self._build_params(fields),
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
            params=self._build_params(fields),
            json_data=self._build_json_data(
                {
                    "video_id": video_id,
                    "max_count": max_count,
                    "cursor": cursor,
                }
            ),
        )

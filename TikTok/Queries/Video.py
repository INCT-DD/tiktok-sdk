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

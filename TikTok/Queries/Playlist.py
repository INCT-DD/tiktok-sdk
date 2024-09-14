"""
This module contains the PlaylistQueries class for handling playlist-related API queries to the TikTok platform.
"""

import httpx
import orjson
import structlog
from pydantic import ValidationError

from TikTok.ValidationModels import Playlist
from TikTok.Exceptions.Query import QueryException

from TikTok.Queries.Common import QueryClass

logger = structlog.get_logger()


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
        headers = Playlist.RequestHeadersModel(
            authorization=await self.query.auth.get_access_token()
        )
        try:
            response: httpx.Response = await self.query.client.post(
                url=self.query.endpoints.PlaylistInfoURL,
                headers=headers.model_dump(by_alias=True),
                json=Playlist.InfoRequestModel(
                    playlist_id=playlist_id,
                    cursor=cursor,
                ).model_dump(exclude_none=True),
            )
            if response.status_code != 200:
                try:
                    return Playlist.InfoResponseModel(**orjson.loads(response.text))
                except ValidationError as e:
                    logger.error(
                        f"The attempted query failed because the response body was invalid: {e}"
                    )
                    raise e
                except Exception as e:
                    logger.error(
                        f"The attempted query failed with the status code {response.status_code}. Details: {e}"
                    )
                    raise QueryException(f"TikTok API query failed. Details: {e}")
            return Playlist.InfoResponseModel(**orjson.loads(response.content))
        except QueryException as e:
            raise e
        except ValidationError as e:
            logger.error(
                f"The attempted query failed because the response body was invalid: {e}"
            )
            raise e
        except Exception as e:
            logger.error(
                f"An unknown exception occurred while querying the TikTok API: {e}"
            )
            raise e

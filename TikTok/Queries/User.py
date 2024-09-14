"""
This module contains the UserQueries class for handling user-related API queries to the TikTok platform.
"""

import httpx
import orjson
import structlog
from pydantic import ValidationError

from TikTok.ValidationModels import User
from TikTok.Exceptions.Query import QueryException

from TikTok.Queries.Common import QueryClass

logger = structlog.get_logger()


class UserQueries(QueryClass):
    """
    A class to handle user-related API queries to the TikTok platform.

    This class inherits from QueryClass and provides methods to interact with the TikTok API
    for retrieving user information.
    """

    async def info(
        self, username: str, fields: list[User.UserInfoQueryFields]
    ) -> User.UserInfoResponseDataModel:
        """
        Retrieves user information based on the provided username and specified fields.

        Parameters:
            username (str): The username of the TikTok user.
            fields (list[User.UserInfoQueryFields]): A list of fields to retrieve from the API.

        Returns:
            User.UserInfoResponseDataModel: The response data model containing user information.

        Raises:
            QueryException: If the API query fails or returns an error.
            ValidationError: If the response body is invalid according to the expected model.
            Exception: For any other unexpected errors that may occur during the API request.
        """
        headers = User.UserInfoRequestHeadersModel(
            authorization=await self.query.auth.get_access_token()
        )
        try:
            response: httpx.Response = await self.query.client.post(
                url=self.query.endpoints.UserInfoURL,
                headers=headers.model_dump(by_alias=True),
                params={"fields": fields},
                json=User.UserInfoRequestModel(
                    username=username,
                ).model_dump(),
            )
            if response.status_code != 200:
                error_message: dict[str, str] = orjson.loads(response.text)

                logger.error(
                    f"The attempted query failed with the status code: {response.status_code} because {error_message['error']['message']}"
                )
                raise QueryException(
                    f"TikTok API query failed because {error_message['error']['message']}"
                )
            return User.UserInfoResponseModel(**orjson.loads(response.content))
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

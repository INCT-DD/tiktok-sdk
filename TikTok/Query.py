"""
Provides the `Query` class, which facilitates interaction with the TikTok API.

The `Query` class is designed to work with an OAuth2 authentication instance and an asynchronous HTTP client 
to perform various API requests, such as retrieving user and playlist information. The module also handles 
error logging and exception management.

Usage:
    1. Authenticate using the `OAuth2` class:
    
    ```python
    from TikTok.Auth import OAuth2
    from TikTok.Types.OAuth2 import RequestHeadersModel, TokenRequestBodyModel

    auth: OAuth2 = await OAuth2.authenticate(
        headers=RequestHeadersModel(),
        body=TokenRequestBodyModel(
            client_key="YOUR_CLIENT_KEY",
            client_secret="YOUR_CLIENT_SECRET",
        ),
    )
    ```

    2. Instantiate the `Query` class with the authenticated `OAuth2` instance:
    
    ```python
    from TikTok.Query import Query

    query = Query(auth)
    ```

    3. Retrieve information:
    
    ```python
    from TikTok.Types.User import QueryFields as UserQueryFields

    user_info = await query.user(
        username="example_username",
        fields=[
            UserQueryFields.display_name,
            UserQueryFields.follower_count,
            UserQueryFields.following_count,
            UserQueryFields.video_count,
            UserQueryFields.likes_count,
        ],
    )
    ```
"""

import httpx
import orjson
import structlog
from pydantic import ValidationError

from TikTok.Types import User, Playlist
from TikTok.Auth import OAuth2
from TikTok.Exceptions.Query import QueryException
from TikTok.Types.RestAPI import APIEndpoints

logger = structlog.get_logger()


class Query:
    """
    A class to interact with the TikTok API.

    This class requires an OAuth2 authentication instance to initialize and uses an
    asynchronous HTTP client to make requests to the TikTok API.

    Attributes:
        client (httpx.AsyncClient): The HTTP client for making API requests.
        auth (OAuth2): The OAuth2 authentication instance.
        endpoints (APIEndpoints): The API endpoints used for making requests.
    """

    client: httpx.AsyncClient
    auth: OAuth2
    endpoints: APIEndpoints

    def __init__(self, auth: OAuth2):
        """
        Initializes the Query class with an OAuth2 authentication instance.

        Parameters:
            auth (OAuth2): An instance of OAuth2 for authentication.
        """
        self.client = httpx.AsyncClient()
        self.auth = auth
        self.endpoints = APIEndpoints()

    async def user(
        self, username: str, fields: list[User.QueryFields]
    ) -> User.ResponseDataModel:
        """
        This method sends a request to the TikTok API to retrieve user information based on the provided username and specified fields.

        Parameters:
            username (str): The username of the TikTok user.
            fields (list[User.QueryFields]): A list of fields to retrieve from the API.

        Returns:
            User.ResponseDataModel: The response data model containing user information.

        Raises:
            QueryException: If the API query fails or returns an error.
            ValidationError: If the response body is invalid according to the expected model.
            Exception: For any other unexpected errors that may occur during the API request.
        """
        headers = User.RequestHeadersModel(
            authorization=await self.auth.get_access_token()
        )
        try:
            response: httpx.Response = await self.client.post(
                url=self.endpoints.UserInfoURL,
                headers=headers.model_dump(by_alias=True),
                params={"fields": fields},
                json=User.InfoRequestModel(
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
            return User.InfoResponseModel(**orjson.loads(response.content))
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

    async def playlist(
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
            authorization=await self.auth.get_access_token()
        )
        try:
            response: httpx.Response = await self.client.post(
                url=self.endpoints.PlaylistInfoURL,
                headers=headers.model_dump(by_alias=True),
                json=Playlist.InfoRequestModel(
                    playlist_id=playlist_id,
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

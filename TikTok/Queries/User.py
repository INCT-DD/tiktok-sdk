"""
This module contains the UserQueries class for handling user-related API queries to the TikTok platform.
"""

from TikTok.ValidationModels import User

from TikTok.Queries.Common import QueryClass, RequestModel, ResponseModel


class UserQueries(QueryClass[RequestModel, ResponseModel]):
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
            TikTok.Exceptions.Query.QueryException: If the API query fails or returns an error.
            pydantic.ValidationError: If the response body is invalid according to the expected model.
            httpx.HTTPError: For any HTTP errors that may occur during the API request.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserInfoURL,
            request_model_class=User.BaseUserInfoRequestModel,
            response_model_class=User.UserInfoResponseModel,
            params=self._build_params(fields),
            json_data={"username": username},
        )

    async def liked_videos(
        self,
        username: str,
        fields: list[User.UserVideosQueryFields],
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> User.UserLikedVideosResponseModel:
        """
        Retrieves a list of videos liked by the specified TikTok user.

        Parameters:
            username (str): The username of the TikTok user whose liked videos are to be retrieved.
            fields (list[User.UserVideosQueryFields]): A list of fields to retrieve from the API.
            max_count (int | None): The maximum number of liked videos to retrieve. Defaults to None.
            cursor (int | None): A cursor for pagination, allowing retrieval of additional liked videos. Defaults to None.

        Returns:
            User.UserLikedVideosResponseModel: The response data model containing the user's liked videos.

        Raises:
            TikTok.Exceptions.Query.QueryException: If the API query fails or returns an error.
            pydantic.ValidationError: If the response body is invalid according to the expected model.
            httpx.HTTPError: For any HTTP errors that may occur during the API request.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserLikedVideosURL,
            request_model_class=User.PaginatedUserInfoRequestModel,
            response_model_class=User.UserLikedVideosResponseModel,
            params=self._build_params(fields),
            json_data=self._build_json_data(
                {
                    "username": username,
                    "max_count": max_count,
                    "cursor": cursor,
                }
            ),
        )

    async def pinned_videos(
        self, username: str, fields: list[User.UserVideosQueryFields]
    ) -> User.UserPinnedVideosResponseModel:
        """
        Retrieves a list of videos pinned by the specified TikTok user.

        Parameters:
            username (str): The username of the TikTok user whose pinned videos are to be retrieved.
            fields (list[User.UserVideosQueryFields]): A list of fields to retrieve from the API.

        Returns:
            User.UserPinnedVideosResponseModel: The response data model containing the user's pinned videos.

        Raises:
            TikTok.Exceptions.Query.QueryException: If the API query fails or returns an error.
            pydantic.ValidationError: If the response body is invalid according to the expected model.
            httpx.HTTPError: For any HTTP errors that may occur during the API request.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserPinnedVideosURL,
            request_model_class=User.PaginatedUserInfoRequestModel,
            response_model_class=User.UserPinnedVideosResponseModel,
            params=self._build_params(fields),
            json_data={"username": username},
        )

    async def reposted_videos(
        self,
        username: str,
        fields: list[User.UserVideosQueryFields],
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> User.UserRepostedVideosResponseModel:
        """
        Retrieves a list of videos reposted by the specified TikTok user.

        Parameters:
            username (str): The username of the TikTok user whose reposted videos are to be retrieved.
            fields (list[User.UserVideosQueryFields]): A list of fields to retrieve from the API.
            max_count (int | None): The maximum number of reposted videos to retrieve. Defaults to None.
            cursor (int | None): A cursor for pagination, allowing retrieval of additional reposted videos. Defaults to None.

        Returns:
            User.UserRepostedVideosResponseModel: The response data model containing the user's reposted videos.

        Raises:
            TikTok.Exceptions.Query.QueryException: If the API query fails or returns an error.
            pydantic.ValidationError: If the response body is invalid according to the expected model.
            httpx.HTTPError: For any HTTP errors that may occur during the API request.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserRepostedVideosURL,
            request_model_class=User.PaginatedUserInfoRequestModel,
            response_model_class=User.UserRepostedVideosResponseModel,
            params=self._build_params(fields),
            json_data=self._build_json_data(
                {
                    "username": username,
                    "max_count": max_count,
                    "cursor": cursor,
                }
            ),
        )

    async def followers(
        self,
        username: str,
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> User.UserFollowersResponseModel:
        """
        Retrieves a list of followers for the specified TikTok user.

        Parameters:
            username (str): The username of the TikTok user whose followers are to be retrieved.
            max_count (int | None): The maximum number of followers to retrieve. Defaults to None.
            cursor (int | None): A cursor for pagination, allowing retrieval of additional followers. Defaults to None.

        Returns:
            User.UserFollowersResponseModel: The response data model containing the user's followers.

        Raises:
            TikTok.Exceptions.Query.QueryException: If the API query fails or returns an error.
            pydantic.ValidationError: If the response body is invalid according to the expected model.
            httpx.HTTPError: For any HTTP errors that may occur during the API request.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserFollowersURL,
            request_model_class=User.PaginatedUserInfoRequestModel,
            response_model_class=User.UserFollowersResponseModel,
            json_data=self._build_json_data(
                {
                    "username": username,
                    "max_count": max_count,
                    "cursor": cursor,
                }
            ),
        )

    async def following(
        self,
        username: str,
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> User.UserFollowingResponseModel:
        """
        Retrieves a list of users the specified TikTok user is following.

        Parameters:
            username (str): The username of the TikTok user whose following are to be retrieved.
            max_count (int | None): The maximum number of users to retrieve. Defaults to None.
            cursor (int | None): A cursor for pagination, allowing retrieval of additional users. Defaults to None.

        Returns:
            User.UserFollowingResponseModel: The response data model containing the user's following.

        Raises:
            TikTok.Exceptions.Query.QueryException: If the API query fails or returns an error.
            pydantic.ValidationError: If the response body is invalid according to the expected model.
            httpx.HTTPError: For any HTTP errors that may occur during the API request.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserFollowingURL,
            request_model_class=User.PaginatedUserInfoRequestModel,
            response_model_class=User.UserFollowingResponseModel,
            json_data=self._build_json_data(
                {
                    "username": username,
                    "max_count": max_count,
                    "cursor": cursor,
                }
            ),
        )

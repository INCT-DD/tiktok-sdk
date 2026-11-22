"""Query public account information and lists through the Research API."""

from TikTok.Queries.Common import QueryClass
from TikTok.ValidationModels import User


class UserQueries(QueryClass):
    """Get public profiles, videos, and lists of accounts."""

    async def info(
        self, username: str, fields: list[User.UserInfoQueryFields]
    ) -> User.UserInfoResponseModel:
        """Get the selected profile fields for a TikTok username.

        Give at least one field. The response contains the profile data and
        the TikTok request log ID. An invalid selection raises ValueError.
        An API or transport failure raises QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserInfoURL,
            response_model_class=User.UserInfoResponseModel,
            params=self._build_params(fields, User.UserInfoQueryFields),
            request=User.BaseUserInfoRequestModel(username=username),
        )

    async def liked_videos(
        self,
        username: str,
        fields: list[User.UserVideosQueryFields],
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> User.UserLikedVideosResponseModel:
        """Get one page of videos liked by the specified account.

        Give at least one video field. The default page size is 20 and the
        maximum is 100. Use data.user_liked_videos to read the records. When
        data.has_more is true, pass data.cursor unchanged to the next call.

        An invalid selection or count raises ValueError. An API or transport
        failure raises QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserLikedVideosURL,
            response_model_class=User.UserLikedVideosResponseModel,
            params=self._build_params(fields, User.UserVideosQueryFields),
            request=User.PaginatedUserInfoRequestModel(
                username=username, max_count=max_count, cursor=cursor
            ),
        )

    async def pinned_videos(
        self, username: str, fields: list[User.UserVideosQueryFields]
    ) -> User.UserPinnedVideosResponseModel:
        """Get the videos pinned to the specified account in one response.

        Give at least one video field. Read the results from
        data.pinned_videos_list. An invalid selection raises ValueError.
        An API or transport failure raises QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserPinnedVideosURL,
            response_model_class=User.UserPinnedVideosResponseModel,
            params=self._build_params(fields, User.UserVideosQueryFields),
            request=User.BaseUserInfoRequestModel(username=username),
        )

    async def reposted_videos(
        self,
        username: str,
        fields: list[User.UserVideosQueryFields],
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> User.UserRepostedVideosResponseModel:
        """Get one page of videos reposted by the specified account.

        Give at least one video field. The default page size is 20 and the
        maximum is 100. Read the videos from data.reposted_videos. When
        data.has_more is true, use data.cursor as the next index.

        An invalid selection or count raises ValueError. An API or transport
        failure raises QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserRepostedVideosURL,
            response_model_class=User.UserRepostedVideosResponseModel,
            params=self._build_params(fields, User.UserVideosQueryFields),
            request=User.PaginatedUserInfoRequestModel(
                username=username, max_count=max_count, cursor=cursor
            ),
        )

    async def followers(
        self,
        username: str,
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> User.UserFollowersResponseModel:
        """Get one page of accounts that follow the specified username.

        The cursor selects follows at or before a UTC timestamp in seconds.
        TikTok starts at the current time when the caller omits the cursor.
        The default page size is 20 and the maximum is 100. The response
        contains data.user_followers, data.cursor, and data.has_more.

        An invalid count raises ValueError. An API or transport failure
        raises QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserFollowersURL,
            response_model_class=User.UserFollowersResponseModel,
            request=User.PaginatedUserInfoRequestModel(
                username=username, max_count=max_count, cursor=cursor
            ),
        )

    async def following(
        self,
        username: str,
        max_count: int | None = None,
        cursor: int | None = None,
    ) -> User.UserFollowingResponseModel:
        """Get one page of accounts followed by the specified username.

        The cursor selects follows at or before a UTC timestamp in seconds.
        TikTok starts at the current time when the caller omits the cursor.
        The default page size is 20 and the maximum is 100. The response
        contains data.user_following, data.cursor, and data.has_more.

        An invalid count raises ValueError. An API or transport failure
        raises QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.UserFollowingURL,
            response_model_class=User.UserFollowingResponseModel,
            request=User.PaginatedUserInfoRequestModel(
                username=username, max_count=max_count, cursor=cursor
            ),
        )

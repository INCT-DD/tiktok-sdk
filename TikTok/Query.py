"""
Provides the `Query` class, which facilitates interaction with the TikTok API.

The `Query` class is designed to work with an OAuth2 authentication instance and an asynchronous HTTP client 
to perform various API requests, such as retrieving user and playlist information. The module also handles 
error logging and exception management.

Usage:
    1. Authenticate using the `OAuth2` class:
    
    ```python
    from TikTok.Auth import OAuth2
    from TikTok.ValidationModels.OAuth2 import RequestHeadersModel, TokenRequestBodyModel

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
    from TikTok.ValidationModels.User import UserInfoQueryFields

    user_info = await query.user.info(
        username="example_username",
        fields=[
            UserInfoQueryFields.display_name,
            UserInfoQueryFields.follower_count,
            UserInfoQueryFields.following_count,
            UserInfoQueryFields.video_count,
            UserInfoQueryFields.likes_count,
        ],
    )
    ```
"""

import httpx
import structlog
from TikTok.Auth import OAuth2
from TikTok.ValidationModels.RestAPI import APIEndpoints

from TikTok.Queries.User import UserQueries
from TikTok.Queries.Playlist import PlaylistQueries

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
    user: UserQueries
    playlist: PlaylistQueries

    def __init__(self, auth: OAuth2):
        """
        Initializes the Query class with an OAuth2 authentication instance.

        Parameters:
            auth (OAuth2): An instance of OAuth2 for authentication.
        """
        self.client = httpx.AsyncClient()
        self.auth = auth
        self.endpoints = APIEndpoints()
        self.user = UserQueries(self)
        self.playlist = PlaylistQueries(self)

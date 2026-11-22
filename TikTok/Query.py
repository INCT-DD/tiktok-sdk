"""Access the public Research API through a single authenticated query client."""

import httpx

from TikTok.Auth import OAuth2
from TikTok.ValidationModels.RestAPI import APIEndpoints

from TikTok.Queries.Compliance import ComplianceQueries
from TikTok.Queries.User import UserQueries
from TikTok.Queries.Playlist import PlaylistQueries
from TikTok.Queries.Video import VideoQueries


class Query:
    """
    Access video, user, playlist, and compliance operations.

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
    video: VideoQueries
    compliance: ComplianceQueries

    def __init__(self, auth: OAuth2) -> None:
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
        self.video = VideoQueries(self)
        self.compliance = ComplianceQueries(self)

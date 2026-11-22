"""Common headers, request validation, and Research API error details."""

from pydantic import BaseModel, ConfigDict, Field
from TikTok.ValidationModels.OAuth2 import AuthorizationHeaderModel


class BaseRequestModel(BaseModel):
    """Reject unrecognized request fields before sending a request."""

    model_config: ConfigDict = ConfigDict(extra="forbid")

    class HeadersModel(AuthorizationHeaderModel):
        """
        Model for request headers specific to user data requests.

        Attributes:
            content_type (str): The content type of the request, defaulting to "application/json".
        """

        content_type: str = Field(default="application/json", alias="Content-Type")


class ResponseErrorModel(BaseModel):
    """
    Model for error information in the API response.

    Attributes:
        code (str): Error code.
        message (str): Error message.
        log_id (str): Log identifier for the error.
        http_status_code (int): HTTP status reported by the service, if supplied.
    """

    code: str | None = None
    message: str | None = None
    log_id: str | None = None
    http_status_code: int | None = None

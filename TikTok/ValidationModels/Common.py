"""
Contains data models shared between all API endpoints.

It defines the structure of error responses returned by the API, ensuring
consistency and clarity in error handling across different endpoints.
"""

from pydantic import Field
from TikTok.ValidationModels.BaseModels import NoExtraFieldsBaseModel


class ResponseErrorModel(NoExtraFieldsBaseModel):
    """
    Model for error information in the API response.

    Attributes:
        code (str): Error code.
        message (str): Error message.
        log_id (str): Log identifier for the error.
    """

    code: str | None = Field(default=None)
    message: str | None = Field(default=None)
    log_id: str | None = Field(default=None)

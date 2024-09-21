"""
This module contains the QueryClass, which serves as a base class for handling common API queries.

The QueryClass is designed to encapsulate shared functionality and attributes for subclasses that interact 
with the TikTok API. It provides a reference to the parent Query instance, allowing subclasses to access 
authentication and endpoint information.

Usage:
    Subclasses can inherit from QueryClass to implement specific API query methods, ensuring 
    consistent handling of API requests and responses.
"""

import httpx
import orjson
import structlog
from pydantic import ValidationError, BaseModel
from cytoolz import curry
from typing import TYPE_CHECKING, TypeVar, Generic, Type, Any

from TikTok.Exceptions.Query import QueryException

logger = structlog.get_logger()

if TYPE_CHECKING:
    from TikTok.Query import Query

RequestModel = TypeVar("RequestModel", bound=BaseModel)
ResponseModel = TypeVar("ResponseModel", bound=BaseModel)


class QueryClass(Generic[RequestModel, ResponseModel]):
    """
    A subclass to handle common API queries.

    Attributes:
        query (Query): The parent Query instance.
    """

    def __init__(self, query: "Query") -> None:
        """
        Initializes the QueryClass subclass with a reference to the parent Query instance.

        Parameters:
            query (Query): The parent Query instance.
        """
        self.query = query

    @curry
    async def _fetch_data(
        self,
        url: str,
        request_model_class: Type[RequestModel],
        response_model_class: Type[ResponseModel],
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> ResponseModel:
        """
        Generalized method to fetch data from the TikTok API.

        This method handles the HTTP POST request, response validation, and error handling.

        Parameters:
            url (str): The API endpoint URL.
            request_model_class (Type[RequestModel]): The Pydantic model class for the request payload.
            response_model_class (Type[ResponseModel]): The Pydantic model class for the response payload.
            params (dict[str, Any] | None): Query parameters for the request. Defaults to None.
            json_data (dict[str, Any] | None): JSON payload for the request. Defaults to None.

        Returns:
            ResponseModel: An instance of the response_model_class containing the API response data.

        Raises:
            QueryException: If the API query fails or returns an error.
            ValidationError: If the response body is invalid according to the expected model.
            Exception: For any other unexpected errors that may occur during the API request.
        """
        headers = request_model_class.HeadersModel(
            authorization=await self.query.auth.get_access_token()
        ).model_dump(by_alias=True)

        try:
            response: httpx.Response = await self.query.client.post(
                url=url,
                headers=headers,
                params=params or {},
                json=request_model_class(**(json_data or {})).model_dump(
                    exclude_none=True
                ),
            )
            try:
                return response_model_class(**orjson.loads(response.content))
            except ValidationError as _:
                error_message: dict[str, Any] = orjson.loads(response.text)
                logger.error(
                    f"API query failed with status {response.status_code}: {error_message['error']['message']}"
                )
                raise QueryException(
                    f"TikTok API query failed because {error_message['error']['message']}"
                )
        except QueryException as e:
            raise e
        except ValidationError as e:
            logger.error(f"Invalid response body: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unknown exception during API query: {e}")
            raise e

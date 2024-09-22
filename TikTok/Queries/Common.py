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
from cytoolz import valfilter
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
            TikTok.Exceptions.Query.QueryException: If the API query fails or returns an error.
            pydantic.ValidationError: If the response body is invalid according to the expected model.
            httpx.HTTPError: For any HTTP errors that may occur during the API request.
        """
        headers: httpx.Headers = httpx.Headers(
            request_model_class.HeadersModel(
                authorization=await self.query.auth.get_access_token()
            ).model_dump(by_alias=True)
        )

        try:
            response: httpx.Response = await self.query.client.post(
                url=url,
                headers=headers,
                params=params or {},
                json=request_model_class(**(json_data or {})).model_dump(
                    exclude_none=True
                ),
            )
            # Whoever made the TikTok API return correct data on 500 status codes should be ashamed of themselves
            # This behavior happens mainly on the Playlist Info endpoint, which I never saw return a single 200 status code before
            if response.is_error and response.status_code < 500:
                response.raise_for_status()
            try:
                return response_model_class(**orjson.loads(response.content))
            except ValidationError:
                error_message: dict[str, Any] = orjson.loads(response.text)
                reason: str = (
                    error_message["error"]["code"]
                    if "code" in error_message["error"]
                    else error_message["error"]["message"]
                )
                logger.error(f"TikTok API query failed: {reason}")
                raise QueryException(f"TikTok API query failed: {reason}")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during API query: {e}")
            raise

    def _build_json_data(self, json_data: dict[str, Any]) -> dict[str, Any]:
        """
        Constructs a JSON-compatible dictionary by filtering out None values from the input data.

        This method takes a dictionary and removes any key-value pairs where the value is None,
        ensuring that the resulting dictionary is suitable for JSON serialization.

        Parameters:
            json_data (dict[str, Any]): The input dictionary containing data to be filtered.

        Returns:
            dict[str, Any]: A new dictionary containing only the key-value pairs with non-None values.

        Example:
            >>> _build_json_data({'key1': 'value1', 'key2': None})
            {'key1': 'value1'}

        Raises:
            TypeError: If the input data is not a dictionary.
        """
        return valfilter(lambda x: x is not None, json_data)

    def _build_params(self, params: list[str]) -> str:
        """
        Converts a list of values into a comma-separated string.

        Parameters:
            params (list[str]): The list of values to be converted into a comma-separated string.

        Returns:
            str: A comma-separated string of the input values.
        """
        return {"fields": ",".join(params)}

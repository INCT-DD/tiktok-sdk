"""Send authenticated Research API requests and validate responses."""

from collections.abc import Sequence
from enum import StrEnum
from json import JSONDecodeError

import httpx
from pydantic import BaseModel, HttpUrl

from TikTok.Exceptions.Query import QueryException
from TikTok.ValidationModels.BaseModels import BaseRequestModel
from TikTok.ValidationModels.OAuth2 import AuthorizationHeaderModel

lazy from TikTok.Query import Query


class QueryClass:
    """Share the authenticated HTTP client across Research API operations."""

    def __init__(self, query: Query) -> None:
        """Use the client, token, and endpoint URLs from the parent query."""
        self.query = query

    async def _post(
        self,
        url: str | HttpUrl,
        *,
        params: dict[str, str] | None = None,
        json_data: dict[str, object] | None = None,
        form: dict[str, str] | None = None,
        files: dict[str, tuple[str, bytes, str]] | None = None,
    ) -> httpx.Response:
        """Send JSON or a multipart form and return the HTTP response.

        HTTPX sets the content type and the multipart boundary. A connection
        error raises QueryException. Each caller decodes the response in the
        format specified for its endpoint.
        """
        headers = AuthorizationHeaderModel(
            authorization=await self.query.auth.get_access_token()
        )
        try:
            return await self.query.client.post(
                str(url),
                headers=headers.model_dump(by_alias=True),
                params=params,
                json=json_data,
                data=form,
                files=files,
            )
        except httpx.RequestError as exc:
            raise QueryException(f"TikTok request failed: {exc}") from exc

    @staticmethod
    def _read_json(response: httpx.Response) -> dict[str, object]:
        """Read the response object and check its HTTP status and TikTok error.

        Raise QueryException for an HTTP failure, an API error, or invalid JSON.
        Preserve the TikTok error code, message, and log ID when available.
        """
        try:
            payload = response.json()
        except (JSONDecodeError, UnicodeDecodeError) as exc:
            raise QueryException(
                f"TikTok returned HTTP {response.status_code} without a JSON response.",
                status_code=response.status_code,
            ) from exc

        if not isinstance(payload, dict):
            raise QueryException(
                "Expected a JSON object from TikTok.", status_code=response.status_code
            )

        details = payload.get("error")
        error = details if isinstance(details, dict) else {}
        code = error.get("code")
        if code not in (None, "", "ok"):
            raise QueryException(
                error.get("message") or str(code),
                status_code=response.status_code,
                code=code,
                log_id=error.get("log_id"),
            )
        if not response.is_success:
            raise QueryException(
                f"TikTok returned HTTP {response.status_code}.",
                status_code=response.status_code,
                log_id=error.get("log_id"),
            )
        return payload

    async def _fetch_data[Result: BaseModel](
        self,
        url: str | HttpUrl,
        request: BaseRequestModel,
        response_model_class: type[Result],
        params: dict[str, str] | None = None,
    ) -> Result:
        """Send a validated JSON request and return its response model.

        Omit optional body fields with a value of None. A successful response
        with the wrong shape raises a Pydantic validation error. HTTP and
        TikTok errors raise QueryException.
        """
        response = await self._post(
            url,
            params=params,
            json_data=request.model_dump(mode="json", by_alias=True, exclude_none=True),
        )
        return response_model_class.model_validate(self._read_json(response))

    @staticmethod
    def _build_params(
        fields: Sequence[str], field_type: type[StrEnum]
    ) -> dict[str, str]:
        """Encode the selected fields. Raise ValueError for an empty or unknown selection."""
        if not fields or isinstance(fields, str):
            raise ValueError("Supply a nonempty sequence of field names.")
        return {"fields": ",".join(map(field_type, fields))}

"""Create Research API compliance tasks and retrieve their results."""

import asyncio
import re
from pathlib import Path

from TikTok.Exceptions.Query import QueryException
from TikTok.Queries.Common import QueryClass
from TikTok.ValidationModels import Compliance


class ComplianceQueries(QueryClass):
    """Check batches of public video or comment IDs."""

    async def create(
        self, category: Compliance.ComplianceCategory, file_data: list[int] | Path
    ) -> Compliance.CreateResponseModel:
        """Submit one to 10,000 video IDs or comment IDs in a single task.

        Supply a list of positive IDs or a path to a UTF-8 text file with
        comma-separated or whitespace-separated IDs. The SDK sends a multipart
        text file. Use data.task_id to check progress. An invalid category or
        ID list raises ValueError. File access errors raise OSError.
        """
        if isinstance(file_data, Path):
            content = await asyncio.to_thread(file_data.read_text, encoding="utf-8-sig")
            if re.search(r"[^0-9,\s]", content):
                raise ValueError("The file must contain decimal video or comment IDs.")
            ids = [int(match.group()) for match in re.finditer(r"[0-9]+", content)]
        else:
            ids = file_data
        request = Compliance.CreateRequestModel.model_validate(
            {"category": Compliance.ComplianceCategory(category), "ids": ids},
            strict=True,
        )
        content_bytes = ",".join(str(item) for item in request.ids).encode("ascii")
        response = await self._post(
            self.query.endpoints.ComplianceCreateURL,
            form={"category": request.category.value},
            files={"file_data": ("ids.txt", content_bytes, "text/plain")},
        )
        return Compliance.CreateResponseModel.model_validate(self._read_json(response))

    async def status(self, task_id: int) -> Compliance.StatusResponseModel:
        """Return the task status for a positive task ID.

        Read data.task_status to determine whether the task is processing,
        completed, or failed. TikTok request failures raise QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.ComplianceStatusURL,
            request_model_class=Compliance.TaskRequestModel,
            response_model_class=Compliance.StatusResponseModel,
            json_data={"task_id": task_id},
        )

    async def download(self, task_id: int) -> bytes:
        """Download the text file of valid IDs for a completed task.

        Return the original file bytes. An empty file contains no valid IDs.
        A failed request or an unexpected JSON response raises QueryException.
        """
        request = Compliance.TaskRequestModel(task_id=task_id)
        response = await self._post(
            self.query.endpoints.ComplianceDownloadURL,
            json_data=request.model_dump(mode="json"),
        )
        if not response.is_success or response.content.lstrip().startswith(b"{"):
            self._read_json(response)
            raise QueryException(
                "TikTok returned JSON in place of the compliance file.",
                status_code=response.status_code,
            )
        return response.content

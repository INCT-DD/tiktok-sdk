"""Request and response models for batch validation of video or comment IDs."""

from enum import StrEnum

from pydantic import BaseModel, Field, PositiveInt

from TikTok.ValidationModels.BaseModels import BaseRequestModel, ResponseErrorModel


class ComplianceCategory(StrEnum):
    """Select the type of ID in a validation task."""

    video = "video"
    comment = "comment"


class ComplianceTaskStatus(StrEnum):
    """Status returned for a batch validation task."""

    processing = "Processing"
    completed = "Completed"
    failed = "Failed"


class CreateRequestModel(BaseRequestModel):
    """Validate one to 10,000 IDs from a single category before upload."""

    category: ComplianceCategory
    ids: list[PositiveInt] = Field(min_length=1, max_length=10_000)


class TaskRequestModel(BaseRequestModel):
    """Identify an existing validation task by its numeric ID."""

    task_id: int = Field(gt=0, strict=True)


class CreateResponseDataModel(BaseModel):
    """ID that the caller can use to check the task or download its result."""

    task_id: int


class CreateResponseModel(BaseModel):
    """Response to the creation of a validation task."""

    data: CreateResponseDataModel
    error: ResponseErrorModel


class StatusResponseDataModel(BaseModel):
    """Current state of the validation task."""

    task_status: ComplianceTaskStatus


class StatusResponseModel(BaseModel):
    """Response to a validation task status request."""

    data: StatusResponseDataModel
    error: ResponseErrorModel

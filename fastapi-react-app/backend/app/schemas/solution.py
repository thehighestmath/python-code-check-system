from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.task import Task
from app.schemas.user import User


class SolutionBase(BaseModel):
    source_code: str = Field(..., min_length=10, max_length=10000)
    task_id: int


class SolutionCreate(SolutionBase):
    pass


class SolutionUpdate(BaseModel):
    source_code: Optional[str] = Field(None, min_length=10, max_length=10000)


class Solution(SolutionBase):
    id: int
    student_id: Optional[int] = None
    is_accepted: bool = False
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    student: Optional[User] = None
    task: Optional[Task] = None

    model_config = {"from_attributes": True}

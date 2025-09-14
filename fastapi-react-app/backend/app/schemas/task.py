from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TestBase(BaseModel):
    input_data: str = Field(..., min_length=1, max_length=1000)
    output_data: str = Field(..., min_length=1, max_length=1000)


class TestCreate(TestBase):
    pass


class Test(TestBase):
    id: int
    task_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10, max_length=5000)
    complexity: str = Field(default="easy", pattern="^(easy|medium|hard)$")
    is_active: bool = True


class TaskCreate(TaskBase):
    tests: List[TestCreate] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10, max_length=5000)
    complexity: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    is_active: Optional[bool] = None


class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tests: List[Test] = []

    model_config = {"from_attributes": True}

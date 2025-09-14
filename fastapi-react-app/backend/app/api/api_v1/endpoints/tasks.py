from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.api.api_v1.endpoints.auth import get_current_user
from app.schemas.user import User
from app.models.task import Task as TaskModel, Test as TestModel

router = APIRouter()


@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    is_active: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retrieve tasks."""
    query = db.query(TaskModel).filter(TaskModel.is_active == is_active)
    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.post("/", response_model=Task)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Create new task."""
    # Create task
    task = TaskModel(
        name=task_in.name,
        description=task_in.description,
        complexity=task_in.complexity,
        is_active=task_in.is_active,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    # Create tests
    for test_data in task_in.tests:
        test = TestModel(
            task_id=task.id,
            input_data=test_data.input_data,
            output_data=test_data.output_data,
        )
        db.add(test)

    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=Task)
def read_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get task by ID."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Update a task."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Delete a task."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

import tempfile
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.solution import Solution, SolutionCreate, SolutionUpdate
from app.api.api_v1.endpoints.auth import get_current_user
from app.schemas.user import User
from app.models.solution import Solution as SolutionModel
from app.models.task import Task as TaskModel, Test as TestModel
from app.services.code_checker import CodeCheckerService, DataInOut

router = APIRouter()


def check_solution_code(solution_id: int, db: Session):
    """Background task to check solution code."""
    solution = db.query(SolutionModel).filter(SolutionModel.id == solution_id).first()
    if not solution:
        return

    # Get task tests
    tests = db.query(TestModel).filter(TestModel.task_id == solution.task_id).all()
    test_cases = [
        DataInOut(input_data=test.input_data.split('\n'), output_data=test.output_data.split('\n')) for test in tests
    ]

    # Write code to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(solution.source_code)
        temp_file = f.name

    try:
        # Check code
        checker = CodeCheckerService()
        result = checker.check_code(temp_file, test_cases)

        # Update solution
        solution.is_accepted = result.verdict
        solution.error_message = result.error_verbose if not result.verdict else None
        db.commit()
    finally:
        # Clean up temp file
        import os

        if os.path.exists(temp_file):
            os.unlink(temp_file)


@router.get("/", response_model=List[Solution])
def read_solutions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retrieve solutions for current user."""
    solutions = (
        db.query(SolutionModel).filter(SolutionModel.student_id == current_user.id).offset(skip).limit(limit).all()
    )
    return solutions


@router.post("/", response_model=Solution)
def create_solution(
    *,
    db: Session = Depends(get_db),
    solution_in: SolutionCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Create new solution."""
    # Check if task exists
    task = db.query(TaskModel).filter(TaskModel.id == solution_in.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Create solution
    solution = SolutionModel(
        student_id=current_user.id,
        task_id=solution_in.task_id,
        source_code=solution_in.source_code,
    )
    db.add(solution)
    db.commit()
    db.refresh(solution)

    # Start background task to check code
    background_tasks.add_task(check_solution_code, solution.id, db)

    return solution


@router.get("/{solution_id}", response_model=Solution)
def read_solution(
    *,
    db: Session = Depends(get_db),
    solution_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get solution by ID."""
    solution = (
        db.query(SolutionModel)
        .filter(SolutionModel.id == solution_id, SolutionModel.student_id == current_user.id)
        .first()
    )
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    return solution


@router.put("/{solution_id}", response_model=Solution)
def update_solution(
    *,
    db: Session = Depends(get_db),
    solution_id: int,
    solution_in: SolutionUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Update a solution."""
    solution = (
        db.query(SolutionModel)
        .filter(SolutionModel.id == solution_id, SolutionModel.student_id == current_user.id)
        .first()
    )
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")

    update_data = solution_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(solution, field, value)

    # Reset status when code is updated
    solution.is_accepted = False
    solution.error_message = None

    db.add(solution)
    db.commit()
    db.refresh(solution)

    # Start background task to check updated code
    background_tasks.add_task(check_solution_code, solution.id, db)

    return solution


@router.delete("/{solution_id}")
def delete_solution(
    *,
    db: Session = Depends(get_db),
    solution_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Delete a solution."""
    solution = (
        db.query(SolutionModel)
        .filter(SolutionModel.id == solution_id, SolutionModel.student_id == current_user.id)
        .first()
    )
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")

    db.delete(solution)
    db.commit()
    return {"message": "Solution deleted successfully"}

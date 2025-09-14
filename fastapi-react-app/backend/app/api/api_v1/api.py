from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, solutions, tasks, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(solutions.router, prefix="/solutions", tags=["solutions"])

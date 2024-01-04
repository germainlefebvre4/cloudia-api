from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils
from app.api.api_v1.endpoints import settings
from app.api.api_v1.endpoints import cloud_projects

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(cloud_projects.router, prefix="/cloud", tags=["cloud_providers"])

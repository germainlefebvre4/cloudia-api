from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# from app.cache.redis import init_redis_pool
# from app.cache.service import MoleculesRepository

# @app.on_event("startup")
# async def startup_event():
#     print("Opening mols bakery...")
#     app.state.redis = await init_redis_pool()
#     app.state.mols_repo = MoleculesRepository(app.state.redis)


# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Closing mols bakery...")
#     await app.state.redis.close()


# @app.get("/health-check")
# async def health_check():
#     try:
#         await app.state.redis.set(str(settings.REDIS_SERVER), settings.up)
#         value = await app.state.redis.get(str(settings.REDIS_SERVER))
#     except Exception:  # noqa: E722
#         print("Sorry no power we can't open bakery...")
#         value = settings.down
#     return {settings.web_server: settings.up, str(settings.REDIS_SERVER): value}

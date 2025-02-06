from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .rest.v1 import AuthResource, VersionResource, EveResource
from app.provider.unternet.appletManager import init_applet_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_applet_manager()
    yield

webServer = FastAPI(lifespan=lifespan)
webServer.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
webServer.include_router(AuthResource.router)
webServer.include_router(VersionResource.router)
webServer.include_router(EveResource.router)

#
# MARK: - API here:
#
@webServer.get("/")
def health_check():
    return {"status": "healthy"}

@webServer.get("/status")
def status():
    return {
        "status": "ok",
        "api-version": "v1"
        }

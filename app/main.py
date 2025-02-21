from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .rest.v1 import AuthResource, VersionResource, EveResource
from .rest.v2 import EveResource as EveResourceV2
from app.provider.unternet.appletManager import init_applet_manager
from app.AnswerEngine import init_answer_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.applet_manager = await init_applet_manager()
    app.state.answer_engine = await init_answer_engine()
    yield

webServer = FastAPI(lifespan=lifespan)
webServer.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=7200,
)
webServer.include_router(AuthResource.router)
webServer.include_router(VersionResource.router)
webServer.include_router(EveResource.router)
webServer.include_router(EveResourceV2.router)

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

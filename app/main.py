from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .rest.v1 import AuthResource, VersionResource, EveResource

webServer = FastAPI()
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

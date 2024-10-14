from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from .rest.v1 import AuthResource, VersionResource, EveResource

webServer = FastAPI()
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

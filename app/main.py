from fastapi import FastAPI
from rest.v1 import ClientDocumentResource


webServer = FastAPI()
webServer.include_router(ClientDocumentResource.router)

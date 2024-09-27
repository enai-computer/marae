from fastapi import FastAPI
from rest.v1 import ClientDocumentResource, AdminResource
from dotenv import load_dotenv

load_dotenv()
webServer = FastAPI()
webServer.include_router(ClientDocumentResource.router)
webServer.include_router(AdminResource.router)

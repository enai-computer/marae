from fastapi import FastAPI
from app.rest.v1 import ClientDocumentResource, AdminResource, SearchResource
from dotenv import load_dotenv

load_dotenv()
webServer = FastAPI()
webServer.include_router(ClientDocumentResource.router)
webServer.include_router(AdminResource.router)
webServer.include_router(SearchResource.router)

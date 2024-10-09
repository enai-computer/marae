from fastapi import FastAPI
from dotenv import load_dotenv
from .rest.v1.Endpoints import router as endpoints_router

load_dotenv()
webServer = FastAPI()
webServer.include_router(endpoints_router)

@webServer.get("/status")
def status():
    return {"status": "ok"}

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
webServer = FastAPI()
# webServer.include_router(Endpoints.router)

@webServer.get("/status")
def status():
    return {"status": "ok"}

@webServer.get("/")
def health_check():
    return {"status": "healthy"}

@webServer.get("/version")
def version():
    return {"version": "0.1"}
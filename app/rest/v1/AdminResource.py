from fastapi import APIRouter, Depends, BackgroundTasks
from uuid import UUID
from typing import Annotated
from app.data.Processors.Transform2VectorDB import Transform2VectorDB

router = APIRouter(prefix="/v1", tags=["v1"])

@router.get("/admin/sync-to-vector-db")
def get_admin_info(background_tasks: BackgroundTasks, processor: Annotated[Transform2VectorDB, Depends(Transform2VectorDB)]):
    background_tasks.add_task(processor.sync_all_to_vector_db)
    return {"status": "ok"}


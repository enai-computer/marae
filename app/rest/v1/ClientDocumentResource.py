from fastapi import APIRouter, Depends, BackgroundTasks
from uuid import UUID
from typing import Annotated
from app.data.Processors.UserDataTransformer import UserDataTransformer
from app.data.Processors.Transform2VectorDB import Transform2VectorDB

router = APIRouter(prefix="/v1", tags=["v1"])

@router.put("/{user_id}/webContent/{web_content_id}")
def update_web_content(user_id: UUID, web_content_id: UUID, web_content: dict, background_tasks: BackgroundTasks, processor: Annotated[UserDataTransformer, Depends(UserDataTransformer)]):
    background_tasks.add_task(processor.processWebcontent, web_content_id, web_content)
    return {"status": "ok"}

@router.put("/{user_id}/note/{note_id}")
def update_note(user_id: UUID, note_id: UUID, note: dict, processor: Annotated[UserDataTransformer, Depends(UserDataTransformer)]):
    processor.processNote(note_id, note)
    return {"status": "ok"}

@router.put("/{user_id}/pdf/{pdf_id}")
def update_pdf(user_id: UUID, pdf_id: UUID, pdf: dict, background_tasks: BackgroundTasks, processor: Annotated[UserDataTransformer, Depends(UserDataTransformer)]):
    background_tasks.add_task(processor.processPdf, pdf_id, pdf)
    return {"status": "ok"}

# Delete
@router.delete("/{user_id}/webContent/{web_content_id}")
def delete_web_content(user_id: UUID, web_content_id: UUID, background_tasks: BackgroundTasks, processor: Annotated[Transform2VectorDB, Depends(Transform2VectorDB)]):
    background_tasks.add_task(processor.delete_document, web_content_id)
    return {"status": "ok"}

@router.delete("/{user_id}/note/{note_id}")
def delete_note(user_id: UUID, note_id: UUID, background_tasks: BackgroundTasks, processor: Annotated[Transform2VectorDB, Depends(Transform2VectorDB)]):
    background_tasks.add_task(processor.delete_document, note_id)
    return {"status": "ok"}

@router.delete("/{user_id}/pdf/{pdf_id}")
def delete_pdf(user_id: UUID, pdf_id: UUID, background_tasks: BackgroundTasks, processor: Annotated[Transform2VectorDB, Depends(Transform2VectorDB)]):
    background_tasks.add_task(processor.delete_document, pdf_id)
    return {"status": "ok"}


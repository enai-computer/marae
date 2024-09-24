from fastapi import APIRouter, Depends
from uuid import UUID
from typing import Annotated
from data.Processors import Processor


router = APIRouter(prefix="/v1", tags=["v1"])

@router.put("/{user_id}/webContent/{web_content_id}")
def update_web_content(user_id: UUID, web_content_id: UUID, web_content: dict):
    return {"status": "ok"}

@router.put("/{user_id}/note/{note_id}")
def update_note(user_id: UUID, note_id: UUID, note: dict, processor: Annotated[Processor, Depends(Processor)]):
    processor.processNote(note)
    return {"status": "ok"}

@router.put("/{user_id}/pdf/{pdf_id}")
def update_pdf(user_id: UUID, pdf_id: UUID, pdf: dict):
    return {"status": "ok"}

# Delete
@router.delete("/{user_id}/webContent/{web_content_id}")
def delete_web_content(user_id: UUID, web_content_id: UUID):
    return {"status": "ok"}

@router.delete("/{user_id}/note/{note_id}")
def delete_note(user_id: UUID, note_id: UUID):
    return {"status": "ok"}

@router.delete("/{user_id}/pdf/{pdf_id}")
def delete_pdf(user_id: UUID, pdf_id: UUID):
    return {"status": "ok"}


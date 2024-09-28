from fastapi import APIRouter, Depends, Request
from uuid import UUID
from typing import Annotated
from app.SpacesSearchEngine import SpacesSearchEngine
from app.AnswerEngine import AnswerEngine

router = APIRouter(prefix="/v1", tags=["v1"])

@router.get("/{user_id}/search")
def search(user_id: UUID, request: Request, search_engine: Annotated[SpacesSearchEngine, Depends(SpacesSearchEngine)]):
    print(f"searching for {request.query_params.get('q')}")
    if request.query_params.get('q') is None:
        return {"error": "query is required"}
    return search_engine.search(request.query_params.get('q'))

@router.get("/{user_id}/answer")
def answer(user_id: UUID, request: Request, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    return answer_engine.get_answer(request.query_params.get('q'), request.query_params.get('space_id'))


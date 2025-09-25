from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from apps.server.app.db import get_session
from apps.server.app.schemas.task_schema import TaskRead, TaskCompletionResponse
from apps.server.app.schemas.pet_schema import PetRead
from apps.server.app.services.task_service import list_today_tasks, complete_task

router = APIRouter()

@router.get("/today", response_model=list[TaskRead])
def get_tasks_today(session: Session = Depends(get_session)):
    try:
        return list_today_tasks(session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{task_id}/complete", response_model=TaskCompletionResponse)
def complete(task_id: int, session: Session = Depends(get_session)):
    try:
        xp, pet = complete_task(session, task_id)
        return TaskCompletionResponse(ok=True, xp_awarded=xp, pet=PetRead.model_validate(pet))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

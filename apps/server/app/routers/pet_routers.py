from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from apps.server.app.db import get_session
from apps.server.app.schemas.pet_schema import PetRead
from apps.server.app.services.pet_service import get_single_pet

router = APIRouter()

@router.get("", response_model=PetRead)
def get_pet(session: Session = Depends(get_session)):
    try:
        return get_single_pet(session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

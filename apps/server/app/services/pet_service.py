from sqlmodel import Session
from apps.server.app.models.pet_model import Pet
from apps.server.app.repositories.pet_repo import get_first_pet


def get_single_pet(session: Session) -> Pet:
    pet = get_first_pet(session)
    if not pet:
        raise ValueError("No pet found")
    return pet

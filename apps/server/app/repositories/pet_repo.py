from sqlmodel import Session, select

from apps.server.app.models.pet_model import Pet


def get_first_pet(session: Session) -> Pet | None:
    """Return the single pet for the MVP (or None if not seeded)."""
    return session.exec(select(Pet)).first()

def get_pet_by_id(session: Session, pet_id: int) -> Pet | None:
    """Lookup a pet by primary key."""
    return session.get(Pet, pet_id)
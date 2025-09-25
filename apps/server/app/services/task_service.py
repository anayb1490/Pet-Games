from sqlmodel import Session
from apps.server.app.repositories.task_repo import get_task_by_id, list_tasks_for_pet
from apps.server.app.repositories.pet_repo import get_pet_by_id, get_first_pet
from apps.server.app.models.pet_model import Pet
from apps.server.app.models.task_model import Task

def list_today_tasks(session: Session) -> list[Task]:
    pet = get_first_pet(session)
    if not pet:
        raise ValueError("No pet found")
    return list_tasks_for_pet(session, pet.id)

def complete_task(session: Session, task_id: int) -> tuple[int, Pet]:
    task = get_task_by_id(session, task_id)
    if not task:
        raise ValueError("Task not found")
    pet = get_pet_by_id(session, task.pet_id)
    if not pet:
        raise ValueError("Pet not found")

    xp_awarded = 0
    if not task.completed:
        task.completed = True
        xp_awarded = task.point_val
        pet.xp += xp_awarded
        pet.streak += 1
        session.add(task)
        session.add(pet)
        session.commit()
        session.refresh(pet)

    return xp_awarded, pet

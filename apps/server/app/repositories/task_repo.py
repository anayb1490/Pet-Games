from sqlmodel import Session, select

from apps.server.app.models.task_model import Task


def list_tasks_for_pet(session: Session, pet_id: int) -> list[Task]:
    """All tasks that belong to a pet."""
    return session.exec(select(Task).where(Task.pet_id == pet_id)).all()

def get_task_by_id(session: Session, task_id: int) -> Task | None:
    """Lookup a task by primary key."""
    return session.get(Task, task_id)

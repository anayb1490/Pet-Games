# apps/server/app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

# NOTE: keeping the fully qualified imports per your setup
from apps.server.app.db import init_db, get_session, engine
from apps.server.app.models.pet_model import Pet          # adjust if your file is pet_model.py
from apps.server.app.models.task_model import Task        # adjust if your file is task_model.py
from apps.server.app.schemas.pet_schema import PetRead
from apps.server.app.schemas.task_schema import TaskRead, TaskCompletionResponse

app = FastAPI(title="PetCare MVP")

# CORS for local dev / Expo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """Create tables and seed one pet + some tasks if empty."""
    init_db()
    with Session(engine) as session:
        pet = session.exec(select(Pet)).first()
        if not pet:
            pet = Pet(name="Miso", species="Dog", age=3)
            session.add(pet)
            session.commit()
            session.refresh(pet)

            session.add_all([
                Task(pet_id=pet.id, name="Feed", description="Breakfast"),
                Task(pet_id=pet.id, name="Walk", description="20 minutes"),
                Task(pet_id=pet.id, name="Meds", description="Daily vitamin"),
            ])
            session.commit()

@app.get("/pet", response_model=PetRead)
def get_pet(session: Session = Depends(get_session)):
    """Return the current pet profile."""
    pet = session.exec(select(Pet)).first()
    if not pet:
        raise HTTPException(status_code=404, detail="No pet found")
    # Return as schema (not raw ORM)
    return PetRead.model_validate(pet)

@app.get("/tasks/today", response_model=list[TaskRead])
def get_tasks(session: Session = Depends(get_session)):
    """Return today's tasks for the pet."""
    pet = session.exec(select(Pet)).first()
    if not pet:
        raise HTTPException(status_code=404, detail="No pet found")
    tasks = session.exec(select(Task).where(Task.pet_id == pet.id)).all()
    # Map each ORM row to the TaskRead schema
    return [TaskRead.model_validate(t) for t in tasks]

@app.post("/tasks/{task_id}/complete", response_model=TaskCompletionResponse)
def complete_task(task_id: int, session: Session = Depends(get_session)):
    """Mark a task complete, award XP once, update streak, return updated pet."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    pet = session.get(Pet, task.pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

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

    return TaskCompletionResponse(ok=True, xp_awarded=xp_awarded, pet=PetRead.model_validate(pet))

from typing import Optional
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pet_id: int = Field(foreign_key="pet.id")
    name: str
    description: str = ""
    point_val: int = 10
    completed: bool = False

from typing import Optional
from sqlmodel import SQLModel, Field

class Pet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    species: str
    age: int
    level: int = 1
    xp: int = 0
    streak: int = 0

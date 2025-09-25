from pydantic import BaseModel

class PetRead(BaseModel):
    id: int
    name: str
    species: str
    age: int
    level: int
    xp: int
    streak: int

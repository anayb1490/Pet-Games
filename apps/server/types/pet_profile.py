from pydantic import BaseModel
import Tasks
class PetProfile(BaseModel):
    id: str
    name: str
    species: str
    age: int
    xp: int = 0
    tasks: list[Task]

from pydantic import BaseModel
from pet_schema import PetRead

class TaskRead(BaseModel):
    id: int
    pet_id: int
    name: str
    description: str
    point_val: int
    completed: bool

class TaskCompletionResponse(BaseModel):
    ok: bool
    xp_awarded: int
    pet: PetRead

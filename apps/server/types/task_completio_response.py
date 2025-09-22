from pydantic import BaseModel
class User(BaseModel):
    ok: bool
    ex_reward: int
    pet: PetProfile
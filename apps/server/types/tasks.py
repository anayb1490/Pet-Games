from pydantic import BaseModel
class Task(BaseModel):
    id: str
    name: str
    description: str
    point_val: int = 5
    completed: bool = False
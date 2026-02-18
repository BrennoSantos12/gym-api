from pydantic import BaseModel


class TrainingResponse(BaseModel):
    id: int
    name: str


                 

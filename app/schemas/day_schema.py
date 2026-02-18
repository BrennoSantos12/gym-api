from pydantic import BaseModel


class DayResponse(BaseModel):
    id: int
    name: str


                 

from pydantic import BaseModel
from typing import Optional


class TrainingPlanCreate(BaseModel):
    user_id: int  
    training_id: int
    day_id: int


class TrainingPlanResponse(BaseModel):
    id: int
    user_id: int
    training_id: int
    day_id: int

    model_config = {"from_attributes": True}

class TrainingPlanUpdate(BaseModel):
    day_id: Optional[int] = None

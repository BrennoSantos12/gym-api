from datetime import date
from pydantic import BaseModel
from typing import Optional


class TrainingSessionCreate(BaseModel):
    user_id: int  
    training_plan_id: int
    performed_date: date 


class TrainingSessionResponse(BaseModel):
    id: int
    user_id: int  
    training_plan_id: int
    performed_date: date

    model_config = {"from_attributes": True}


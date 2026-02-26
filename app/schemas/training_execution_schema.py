from pydantic import BaseModel
from typing import Optional


class TrainingExecutionCreate(BaseModel):
    training_session_id: int
    training_plan_exercise_id: int
    sets_done: int
    reps: float
    weight: float


class TrainingExecutionResponse(BaseModel):
    id: int
    training_session_id: int
    training_plan_exercise_id: int
    sets_done: int
    reps: float
    weight: float

    model_config = {"from_attributes": True}



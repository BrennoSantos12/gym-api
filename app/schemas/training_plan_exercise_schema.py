from pydantic import BaseModel
from typing import Optional


class TrainingPlanExerciseCreate(BaseModel):
    training_plan_id: int
    exercise_id: int


class TrainingPlanExerciseResponse(BaseModel):
    id: int
    training_plan_id: int
    exercise_id: int

    model_config = {"from_attributes": True}

class TrainingPlanExerciseUpdate(BaseModel):
    exercise_id: Optional[int] = None

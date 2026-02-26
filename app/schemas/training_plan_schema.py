from pydantic import BaseModel
from typing import Optional
from app.schemas.training_plan_exercise_schema import TrainingPlanExerciseResponse


class TrainingPlanExerciseInput(BaseModel):
    exercise_id: int


class TrainingPlanCreate(BaseModel):
    user_id: int
    training_id: int
    day_id: int
    exercises: list[TrainingPlanExerciseInput] = []


class ReportTrainingPlanResponse(BaseModel):
    id: int
    user_id: int
    training_name: str
    day_name: str


class TrainingPlanResponse(BaseModel):
    id: int
    user_id: int
    training_id: int
    day_id: int
    training_plan_exercises: list[TrainingPlanExerciseResponse] = []

    model_config = {"from_attributes": True}


class TrainingPlanUpdate(BaseModel):
    day_id: Optional[int] = None
    exercises: Optional[list[TrainingPlanExerciseInput]] = None

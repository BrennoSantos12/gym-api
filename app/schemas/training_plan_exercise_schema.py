from pydantic import BaseModel, model_validator
from typing import Optional, Any


class TrainingPlanExerciseCreate(BaseModel):
    training_plan_id: int
    exercise_id: int


class TrainingPlanExerciseResponse(BaseModel):
    id: int
    training_plan_id: int
    exercise_id: int
    exercise_name: str = ""

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def extract_exercise_name(cls, data: Any) -> Any:
        if hasattr(data, "exercise") and data.exercise:
            return {
                "id": data.id,
                "training_plan_id": data.training_plan_id,
                "exercise_id": data.exercise_id,
                "exercise_name": data.exercise.name,
            }
        return data


class TrainingPlanExerciseUpdate(BaseModel):
    exercise_id: Optional[int] = None

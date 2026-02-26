from datetime import date
from typing import Optional
from pydantic import BaseModel


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


class TrainingExecutionCreateInline(BaseModel):
    training_plan_exercise_id: int
    sets_done: int
    reps: float
    weight: float


class TrainingSessionWithExecutionsCreate(BaseModel):
    user_id: int
    training_plan_id: int
    performed_date: date
    executions: list[TrainingExecutionCreateInline]


class TrainingExecutionResponseInline(BaseModel):
    id: int
    training_session_id: int
    training_plan_exercise_id: int
    sets_done: int
    reps: float
    weight: float

    model_config = {"from_attributes": True}


class TrainingSessionWithExecutionsResponse(BaseModel):
    id: int
    user_id: int
    training_plan_id: int
    performed_date: date
    training_executions: list[TrainingExecutionResponseInline]

    model_config = {"from_attributes": True}


class TrainingSessionTodayResponse(BaseModel):
    exists: bool


class TrainingSessionFirstDateResponse(BaseModel):
    first_date: date | None


class TrainingExecutionUpdateInline(BaseModel):
    training_plan_exercise_id: int
    sets_done: Optional[int] = None
    reps: Optional[float] = None
    weight: Optional[float] = None


class TrainingSessionUpdate(BaseModel):
    performed_date: Optional[date] = None
    executions: Optional[list[TrainingExecutionUpdateInline]] = None


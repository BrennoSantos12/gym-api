from pydantic import BaseModel, ConfigDict


class ExerciseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str


class PaginatedExerciseResponse(BaseModel):
    items: list[ExerciseResponse]
    total: int
    page: int
    limit: int
    pages: int

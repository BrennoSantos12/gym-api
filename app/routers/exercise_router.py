import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.exercise_model import Exercise
from app.schemas.exercise_schema import ExerciseResponse, PaginatedExerciseResponse

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("/", response_model=PaginatedExerciseResponse)
def get_exercises(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = Query(None, min_length=1),
    type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Exercise)
    if name:
        query = query.filter(Exercise.name.ilike(f"%{name}%"))
    if type:
        query = query.filter(Exercise.type == type)
    total = query.count()
    items = query.order_by(Exercise.name.asc()).offset((page - 1) * limit).limit(limit).all()
    return PaginatedExerciseResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=math.ceil(total / limit) if total > 0 else 1,
    )

@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    return exercise

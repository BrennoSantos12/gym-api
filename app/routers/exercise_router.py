from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.exercise_model import Exercise
from app.schemas.exercise_schema import ExerciseResponse

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("/", response_model=list[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    exercises = db.query(Exercise).all()
    return exercises

@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    return exercise

@router.get("/type/{type}", response_model=list[ExerciseResponse])
def get_exercise_type(type: str, db: Session = Depends(get_db)):
    exercises = db.query(Exercise).filter(Exercise.type == type).all()
    return exercises

@router.get("/search/", response_model=list[ExerciseResponse])
def search_exercise(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    exercises = db.query(Exercise).filter(Exercise.name.ilike(f"%{name}%")).order_by(Exercise.name.asc()).all()
    return exercises

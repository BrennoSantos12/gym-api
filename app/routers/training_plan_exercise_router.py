from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.training_plan_exercise_model import TrainingPlanExercise
from app.schemas.training_plan_exercise_schema import TrainingPlanExerciseCreate, TrainingPlanExerciseResponse, TrainingPlanExerciseUpdate


router = APIRouter(prefix="/training_plan_exercises", tags=["TrainingPlanExercises"])



@router.post("/", response_model=list[TrainingPlanExerciseResponse])
def create_training_plan_exercise(items: list[TrainingPlanExerciseCreate], db: Session = Depends(get_db)):
    if not items:
         raise HTTPException(status_code=400, detail="Lista vazia.")

    objs = [TrainingPlanExercise(**item.model_dump()) for item in items]

    db.add_all(objs)
    db.commit() 
    
    for obj in objs:
        db.refresh(obj)

    return  objs 


@router.get("/{training_plan_id}", response_model=list[TrainingPlanExerciseResponse])
def get_training_plan_exercise_by_training_plan(training_plan_id: int, db: Session = Depends(get_db)):
    exercises = db.query(TrainingPlanExercise).filter(TrainingPlanExercise.training_plan_id == training_plan_id).all()
    return exercises


@router.put("/{training_plan_exercise_id}", response_model=TrainingPlanExerciseResponse)
def edit_training_plan_exercise(training_plan_exercise_id: int, training_plan_exercise_data: TrainingPlanExerciseUpdate, db: Session = Depends(get_db)):
    training_plan_exercise = db.query(TrainingPlanExercise).filter(TrainingPlanExercise.id == training_plan_exercise_id).first()
    if not training_plan_exercise:
        raise HTTPException(status_code=404, detail="Exercicio da ficha de treino não encontrado.")
    update_data = training_plan_exercise_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(training_plan_exercise, field, value)
    db.commit()
    db.refresh(training_plan_exercise)
    return training_plan_exercise

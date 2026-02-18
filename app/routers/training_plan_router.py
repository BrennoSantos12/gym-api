from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.training_plan_exercise_model import TrainingPlanExercise
from app.models.training_plan_model import TrainingPlan
from app.schemas.training_plan_exercise_schema import TrainingPlanExerciseResponse
from app.schemas.training_plan_schema import TrainingPlanCreate, TrainingPlanResponse, TrainingPlanUpdate

router = APIRouter(prefix="/training_plans", tags=["TrainingPlans"])


@router.post("/", response_model=TrainingPlanResponse)
def create_training_plan(training_plan: TrainingPlanCreate, db: Session = Depends(get_db)):
    data = training_plan.model_dump()
    new_training_plan = TrainingPlan(**data)
    db.add(new_training_plan)
    db.commit()
    db.refresh(new_training_plan)
    return new_training_plan


@router.put("/{training_plan_id}", response_model=TrainingPlanResponse)
def edit_training_plan(training_plan_id: int, training_plan_data: TrainingPlanUpdate , db: Session = Depends(get_db)):
    training_plan = db.query(TrainingPlan).filter(TrainingPlan.id == training_plan_id).first()
    if not training_plan:
        raise HTTPException(status_code=404, detail="Ficha de treino não encontrada.")
    update_data = training_plan_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(training_plan, field, value)
    db.commit()
    db.refresh(training_plan)
    return training_plan


@router.get("/{training_plan_id}", response_model=list[TrainingPlanExerciseResponse])
def get_all_exercises(training_plan_id: int, db: Session = Depends(get_db)):
    all_exercises = db.query(TrainingPlanExercise).filter(TrainingPlanExercise.training_plan_id == training_plan_id).all()

    return all_exercises




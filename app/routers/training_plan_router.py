from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.training_plan_exercise_model import TrainingPlanExercise
from app.models.training_plan_model import TrainingPlan
from app.models.user_model import User
from app.models.day_model import Day
from app.models.training_model import Training
from app.schemas.training_plan_exercise_schema import TrainingPlanExerciseResponse
from app.schemas.training_plan_schema import TrainingPlanCreate, TrainingPlanResponse, TrainingPlanUpdate, ReportTrainingPlanResponse

router = APIRouter(prefix="/training_plans", tags=["TrainingPlans"])


@router.post("/", response_model=TrainingPlanResponse)
def create_training_plan(training_plan: TrainingPlanCreate, db: Session = Depends(get_db)):
    exercises = training_plan.exercises
    data = training_plan.model_dump(exclude={"exercises"})
    new_training_plan = TrainingPlan(**data)
    db.add(new_training_plan)
    db.flush()

    for exercise in exercises:
        new_exercise = TrainingPlanExercise(
            training_plan_id=new_training_plan.id,
            exercise_id=exercise.exercise_id
        )
        db.add(new_exercise)

    db.commit()
    db.refresh(new_training_plan)
    return new_training_plan

@router.get("/user_trainings/name/{user_id}", response_model=list[ReportTrainingPlanResponse])
def get_user_training_name(user_id: int, db: Session = Depends(get_db)):
    trainings = db.query(
        TrainingPlan.id.label("id"),
        Training.name.label("training_name"),
        Day.name.label("day_name"),
        TrainingPlan.user_id.label("user_id")
    ).join(Training, Training.id == TrainingPlan.training_id).join(Day, Day.id == TrainingPlan.day_id).filter(TrainingPlan.user_id == user_id).all()
    return trainings

@router.get("/user_trainings/today/{user_id}", response_model=ReportTrainingPlanResponse)
def get_user_training_today(user_id: int, db: Session = Depends(get_db)):
    cuiaba = datetime.now(ZoneInfo("America/Cuiaba"))
    dia = cuiaba.weekday()
    day_id = dia + 1
    trainings = db.query(
        TrainingPlan.id.label("id"),
        Training.name.label("training_name"),
        Day.name.label("day_name"),
        TrainingPlan.user_id.label("user_id")
    ).join(Training, Training.id == TrainingPlan.training_id).join(Day, Day.id == TrainingPlan.day_id).filter(TrainingPlan.user_id == user_id, TrainingPlan.day_id == day_id).first()
    return trainings


@router.get("/{training_plan_id}", response_model=list[TrainingPlanExerciseResponse])
def get_all_exercises(training_plan_id: int, db: Session = Depends(get_db)):
    all_exercises = db.query(TrainingPlanExercise).filter(TrainingPlanExercise.training_plan_id == training_plan_id).all()

    return all_exercises


@router.put("/{training_plan_id}", response_model=TrainingPlanResponse)
def edit_training_plan(training_plan_id: int, training_plan_data: TrainingPlanUpdate, db: Session = Depends(get_db)):
    training_plan = db.query(TrainingPlan).filter(TrainingPlan.id == training_plan_id).first()
    if not training_plan:
        raise HTTPException(status_code=404, detail="Ficha de treino não encontrada.")

    update_data = training_plan_data.model_dump(exclude_unset=True, exclude={"exercises"})
    for field, value in update_data.items():
        setattr(training_plan, field, value)

    if training_plan_data.exercises is not None:
        new_exercise_ids = {e.exercise_id for e in training_plan_data.exercises}
        existing_by_exercise_id = {ex.exercise_id: ex for ex in training_plan.training_plan_exercises}

        for exercise_id, ex in existing_by_exercise_id.items():
            if exercise_id not in new_exercise_ids:
                db.delete(ex)

        for exercise in training_plan_data.exercises:
            if exercise.exercise_id not in existing_by_exercise_id:
                db.add(TrainingPlanExercise(
                    training_plan_id=training_plan.id,
                    exercise_id=exercise.exercise_id
                ))

    db.commit()
    db.refresh(training_plan)
    return training_plan


@router.delete("/{training_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training_plan(training_plan_id: int, db: Session = Depends(get_db)):
    training_plan = db.query(TrainingPlan).filter(TrainingPlan.id == training_plan_id).first()
    if not training_plan:
        raise HTTPException(status_code=404, detail="Ficha de treino não encontrada.")
    db.delete(training_plan)
    db.commit()

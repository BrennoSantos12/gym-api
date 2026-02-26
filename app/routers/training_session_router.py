from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.training_session_model import TrainingSession
from app.models.training_execution_model import TrainingExecution
from app.schemas.training_session_schema import (
    TrainingSessionCreate,
    TrainingSessionResponse,
    TrainingSessionWithExecutionsCreate,
    TrainingSessionWithExecutionsResponse,
    TrainingSessionTodayResponse,
    TrainingSessionFirstDateResponse,
    TrainingSessionUpdate,
)

router = APIRouter(prefix="/training_sessions", tags=["TrainingSessions"])


@router.post("/", response_model=TrainingSessionResponse)
def post_training_session(items: TrainingSessionCreate, db: Session = Depends(get_db)):
    new_training_session = TrainingSession(**items.model_dump())
    db.add(new_training_session)
    db.commit()
    db.refresh(new_training_session)
    return new_training_session


@router.post("/with_executions", response_model=TrainingSessionWithExecutionsResponse)
def post_training_session_with_executions(
    items: TrainingSessionWithExecutionsCreate, db: Session = Depends(get_db)
):
    executions_data = items.executions
    session_data = items.model_dump(exclude={"executions"})

    new_session = TrainingSession(**session_data)
    db.add(new_session)
    db.flush()

    for execution in executions_data:
        new_execution = TrainingExecution(
            training_session_id=new_session.id,
            **execution.model_dump(),
        )
        db.add(new_execution)

    db.commit()
    db.refresh(new_session)
    return new_session


@router.get("/today/{training_plan_id}", response_model=TrainingSessionTodayResponse)
def get_training_session_today(training_plan_id: int, db: Session = Depends(get_db)):
    today = date.today()
    session = db.query(TrainingSession).filter(
        TrainingSession.training_plan_id == training_plan_id,
        TrainingSession.performed_date == today,
    ).first()
    return TrainingSessionTodayResponse(exists=session is not None)


@router.get("/this_week/{training_plan_id}", response_model=TrainingSessionTodayResponse)
def get_training_session_this_week(training_plan_id: int, db: Session = Depends(get_db)):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    session = db.query(TrainingSession).filter(
        TrainingSession.training_plan_id == training_plan_id,
        TrainingSession.performed_date >= start_of_week,
        TrainingSession.performed_date <= end_of_week,
    ).first()
    return TrainingSessionTodayResponse(exists=session is not None)


@router.get("/first_date/{training_plan_id}", response_model=TrainingSessionFirstDateResponse)
def get_first_training_session_date(training_plan_id: int, db: Session = Depends(get_db)):
    session = (
        db.query(TrainingSession)
        .filter(TrainingSession.training_plan_id == training_plan_id)
        .order_by(TrainingSession.performed_date.asc())
        .first()
    )
    return TrainingSessionFirstDateResponse(first_date=session.performed_date if session else None)


@router.get("/user/{user_id}", response_model=list[TrainingSessionResponse])
def get_training_sessions_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(TrainingSession).filter(TrainingSession.user_id == user_id).all()


@router.delete("/user/{user_id}", status_code=204)
def delete_training_sessions_by_user(user_id: int, db: Session = Depends(get_db)):
    db.query(TrainingSession).filter(TrainingSession.user_id == user_id).delete()
    db.commit()


@router.get("/{training_plan_id}", response_model=list[TrainingSessionResponse])
def get_training_sessions(training_plan_id: int, db: Session = Depends(get_db)):
    training_sessions = db.query(TrainingSession).filter(TrainingSession.training_plan_id == training_plan_id).all()
    return training_sessions


@router.put("/{session_id}", response_model=TrainingSessionWithExecutionsResponse)
def edit_training_session(session_id: int, data: TrainingSessionUpdate, db: Session = Depends(get_db)):
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sessão de treino não encontrada.")

    if data.performed_date is not None:
        session.performed_date = data.performed_date

    if data.executions is not None:
        new_execs_by_exercise = {e.training_plan_exercise_id: e for e in data.executions}
        existing_by_exercise = {ex.training_plan_exercise_id: ex for ex in session.training_executions}

        for exercise_id, ex in existing_by_exercise.items():
            if exercise_id not in new_execs_by_exercise:
                db.delete(ex)
            else:
                update = new_execs_by_exercise[exercise_id]
                if update.sets_done is not None:
                    ex.sets_done = update.sets_done
                if update.reps is not None:
                    ex.reps = update.reps
                if update.weight is not None:
                    ex.weight = update.weight

        for exercise_id, update in new_execs_by_exercise.items():
            if exercise_id not in existing_by_exercise:
                db.add(TrainingExecution(
                    training_session_id=session.id,
                    training_plan_exercise_id=exercise_id,
                    sets_done=update.sets_done,
                    reps=update.reps,
                    weight=update.weight,
                ))

    db.commit()
    db.refresh(session)
    return session

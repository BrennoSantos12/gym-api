from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.training_session_model import TrainingSession
from app.schemas.training_session_schema import TrainingSessionCreate, TrainingSessionResponse

router = APIRouter(prefix="/training_sessions", tags=["TrainingSessions"])


@router.post("/", response_model=TrainingSessionResponse)
def post_training_session(items: TrainingSessionCreate, db: Session = Depends(get_db)):
    new_training_session = TrainingSession(**items.model_dump())
    db.add(new_training_session)
    db.commit()
    db.refresh(new_training_session)
    return new_training_session


@router.get("/{training_plan_id}", response_model=list[TrainingSessionResponse])
def get_training_sessions(training_plan_id: int, db: Session = Depends(get_db)):
    training_sessions = db.query(TrainingSession).filter(TrainingSession.training_plan_id == training_plan_id).all()
    return training_sessions

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.training_model import Training
from app.schemas.training_schema import TrainingResponse

router = APIRouter(prefix="/trainings", tags=["Trainings"])

@router.get("/", response_model=list[TrainingResponse])
def get_trainings(db: Session = Depends(get_db)):
    trainings = db.query(Training).all()
    return trainings

@router.get("/{training_id}", response_model=TrainingResponse)
def get_training(training_id: int, db: Session = Depends(get_db)):
    training = db.query(Training).filter(Training.id == training_id).first()
    return training

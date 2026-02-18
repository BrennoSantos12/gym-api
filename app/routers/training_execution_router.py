from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.training_execution_model import TrainingExecution
from app.schemas.training_execution_schema import TrainingExecutionCreate, TrainingExecutionResponse

router = APIRouter(prefix="/training_executions", tags=["TrainingExecutions"])


@router.post("/", response_model=list[TrainingExecutionResponse])
def post_training_execution(items: list[TrainingExecutionCreate], db: Session = Depends(get_db)):
    new_executions = []
    for item in items:
        new_execution = TrainingExecution(**item.model_dump())
        db.add(new_execution)
        new_executions.append(new_execution)

    db.commit()

    for execution in new_executions:
        db.refresh(execution)

    return new_executions


@router.get("/{training_session_id}", response_model=list[TrainingExecutionResponse])
def get_training_executions(training_session_id: int, db: Session = Depends(get_db)):
    training_executions = db.query(TrainingExecution).filter(TrainingExecution.training_session_id == training_session_id).all()
    return training_executions

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.day_model import Day
from app.models.user_model import User
from app.schemas.day_schema import DayResponse

router = APIRouter(prefix="/days", tags=["Days"])

@router.get("/", response_model=list[DayResponse])
def get_days(db: Session = Depends(get_db)):
    days = db.query(Day).all()
    return days

@router.get("/{day_id}", response_model=DayResponse)
def get_day(
    day_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    day = db.query(Day).filter(Day.id == day_id).first()
    return day

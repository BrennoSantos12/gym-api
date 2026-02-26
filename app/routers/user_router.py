from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.training_plan_model import TrainingPlan
from app.models.user_model import User

from app.schemas.training_plan_schema import TrainingPlanResponse, ReportTrainingPlanResponse
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/today_training/{user_id}", response_model=TrainingPlanResponse)
def get_today_training(user_id: int, db: Session = Depends(get_db)):
    cuiaba = datetime.now(ZoneInfo("America/Cuiaba"))
    dia = cuiaba.weekday()
    day_id = dia + 1
    training_plan = db.query(TrainingPlan).filter(TrainingPlan.user_id == user_id, TrainingPlan.day_id == day_id).first()
    if not training_plan:
         raise HTTPException(status_code=404, detail="Sem treinos pra hoje, bom descanso.")
    return training_plan


@router.get("/user_trainings/{user_id}", response_model=list[TrainingPlanResponse])
def get_user_trainings(user_id: int, db: Session = Depends(get_db)):
    trainings = db.query(TrainingPlan).filter(TrainingPlan.user_id == user_id).all()
    return trainings




@router.post("/", response_model=UserResponse)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    from app.core.security import hash_password
    user_data = user.model_dump()
    user_data["password"] = hash_password(user_data["password"])
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def put_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    from app.core.security import hash_password
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    update_data = user_data.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Esse usuário não existe.")
    db.delete(user)
    db.commit()

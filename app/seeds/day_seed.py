from sqlalchemy.orm import Session
from app.models.day_model import Day

DAYS = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]

def seed_days(db: Session):
    exists = db.query(Day).first()
    if exists:
        return  

    for name in DAYS:
        db.add(Day(name=name))

    db.commit()

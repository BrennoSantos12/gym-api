from sqlalchemy.orm import Session
from app.models.training_model import Training 

TRAININGS = [
    "Treino 1",
    "Treino 2",
    "Treino 3",
    "Treino 4",
    "Treino 5",
    "Treino 6",
    "Trenio 7",
]

def seed_trainings(db: Session):
    exists = db.query(Training).first()
    if exists:
        return  

    for name in TRAININGS:
        db.add(Training(name=name))

    db.commit()

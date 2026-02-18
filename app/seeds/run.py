from app.database import SessionLocal
from app.seeds.day_seed import seed_days
from app.seeds.exercise_seed import seed_exercises
from app.seeds.training_seed import seed_trainings 

def run_seeds():
    db = SessionLocal()
    try:
        seed_days(db)
        seed_exercises(db)
        seed_trainings(db)
    finally:
        db.close()

if __name__ == "__main__":
    run_seeds()

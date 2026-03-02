from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", name="uq_exercises_name"),
    )


    training_plan_exercises = relationship("TrainingPlanExercise",  back_populates="exercise")

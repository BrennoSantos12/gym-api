from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from app.database import Base


class TrainingPlanExercise(Base):
        __tablename__ = "training_plan_exercises"


        id = Column(Integer, primary_key=True, index=True)
        training_plan_id = Column(Integer, ForeignKey("training_plans.id"), nullable=False)
        exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    

        training_plan = relationship("TrainingPlan", back_populates="training_plan_exercises")
        exercise = relationship("Exercise", back_populates="training_plan_exercises")
        training_executions = relationship("TrainingExecution", back_populates="training_plan_exercise")

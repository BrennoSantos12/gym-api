from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from app.database import Base


class TrainingPlan(Base):
        __tablename__ = "training_plans"


        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        training_id = Column(Integer, ForeignKey("trainings.id"), nullable=False)
        day_id = Column(Integer, ForeignKey("days.id"), nullable=False)
    

        user = relationship("User", back_populates="training_plans")
        training = relationship("Training", back_populates="training_plans")
        day = relationship("Day", back_populates="training_plans")

        training_plan_exercises = relationship("TrainingPlanExercise", back_populates="training_plan", cascade="all, delete-orphan")
        training_sessions = relationship("TrainingSession", back_populates="training_plan", cascade="all, delete-orphan")

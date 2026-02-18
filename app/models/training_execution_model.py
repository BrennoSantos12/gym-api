
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class TrainingExecution(Base):
    __tablename__ = "training_executions"

    id = Column(Integer, primary_key=True, index=True)
    training_session_id = Column(Integer, ForeignKey("training_sessions.id"), nullable=False)
    training_plan_exercise_id = Column(Integer, ForeignKey("training_plan_exercises.id"), nullable=False)
    sets_done = Column(Integer, nullable=True)
    reps = Column(Integer,nullable=True)
    weight = Column(Integer, nullable=True)


    training_session = relationship("TrainingSession", back_populates="training_executions")
    training_plan_exercise = relationship("TrainingPlanExercise", back_populates="training_executions")




from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from app.database import Base


class TrainingExecution(Base):
    __tablename__ = "training_executions"

    id = Column(Integer, primary_key=True, index=True)
    training_session_id = Column(Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    training_plan_exercise_id = Column(Integer, ForeignKey("training_plan_exercises.id", ondelete="CASCADE"), nullable=False)
    sets_done = Column(Integer, nullable=True)
    reps = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)


    training_session = relationship("TrainingSession", back_populates="training_executions")
    training_plan_exercise = relationship("TrainingPlanExercise", back_populates="training_executions")



from sqlalchemy import Column, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from app.database import Base


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    training_plan_id = Column(Integer, ForeignKey("training_plans.id", ondelete="CASCADE"), nullable=False)
    performed_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="training_sessions")
    training_plan = relationship("TrainingPlan", back_populates="training_sessions")
    training_executions = relationship("TrainingExecution", back_populates="training_session", cascade="all, delete-orphan")



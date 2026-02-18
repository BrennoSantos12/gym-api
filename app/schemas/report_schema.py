from pydantic import BaseModel
from typing import Optional


class TrainingPlanReportItem(BaseModel):
    training_plan_id: int
    training_id: int
    day_id: int
    planned_total: int
    done_right_day: int
    done_early: int
    done_wrong_day: int
    not_done: int


class ExerciseExecutionStats(BaseModel):
    """Estatísticas de uma execução específica"""
    sets_done: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[int] = None
    performed_date: str  # ISO format


class ExerciseProgressReport(BaseModel):
    """Relatório de progresso de um exercício específico"""
    exercise_id: int
    exercise_name: str
    exercise_type: str
    times_performed: int  # quantas vezes executou
    times_skipped: int  # quantas sessões pulou
    first_execution: Optional[ExerciseExecutionStats] = None  # primeira vez
    best_execution: Optional[ExerciseExecutionStats] = None  # recorde pessoal 
    last_execution: Optional[ExerciseExecutionStats] = None  # mais recente
    improvement_summary: Optional[str] = None  # texto descrevendo a melhora
    improvement_percentage: Optional[float] = None  # % de evolução do volume total


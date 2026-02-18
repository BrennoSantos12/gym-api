from datetime import date, timedelta
from typing import cast
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.schemas.report_schema import (
    TrainingPlanReportItem,
    ExerciseProgressReport,
    ExerciseExecutionStats,
)
from app.models.training_plan_model import TrainingPlan
from app.models.training_session_model import TrainingSession
from app.models.training_plan_exercise_model import TrainingPlanExercise
from app.models.training_execution_model import TrainingExecution
from app.models.exercise_model import Exercise


router = APIRouter(prefix="/reports", tags=["Reports"])



def iso_week_start(d: date) -> date:
    # ISO: Monday=1 ... Sunday=7
    return d - timedelta(days=d.isoweekday() - 1)

def planned_date_in_week(any_day_in_week: date, plan_day_id: int) -> date:
    # devolve a data planejada do plano dentro daquela semana
    week_start = iso_week_start(any_day_in_week)  # segunda
    return week_start + timedelta(days=plan_day_id - 1)

@router.get("/plan-adherence", response_model=list[TrainingPlanReportItem])
def report_plan_adherence(
    user_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    if start_date > end_date:
        raise HTTPException(400, "start_date não pode ser maior que end_date")

    # 1) pega os planos do usuário
    plans = (
        db.query(TrainingPlan)
        .filter(TrainingPlan.user_id == user_id)
        .all()
    )

    if not plans:
        return []

    plan_ids = [p.id for p in plans]

    # 2) pega as sessions do período para esses planos
    sessions = (
        db.query(TrainingSession)
        .filter(
            TrainingSession.user_id == user_id,
            TrainingSession.training_plan_id.in_(plan_ids),
            TrainingSession.performed_date.between(start_date, end_date),
        )
        .all()
    )

    # 3) indexa sessions por plan
    sessions_by_plan: dict[int, list[TrainingSession]] = {}
    for s in sessions:
        sessions_by_plan.setdefault(cast(int, s.training_plan_id), []).append(s)

    # helper: iterar dias
    def iter_dates(a: date, b: date):
        cur = a
        while cur <= b:
            yield cur
            cur += timedelta(days=1)

    report: list[TrainingPlanReportItem] = []

    for p in plans:
        # 4) total planejado no período (conta quantos dias batem com day_id)
        plan_day_id = cast(int, p.day_id)
        planned_total = sum(1 for d in iter_dates(start_date, end_date) if d.isoweekday() == plan_day_id)

        done_right = 0
        done_early = 0
        done_wrong = 0

        # (opcional, mas recomendado) evitar contar duplicado no mesmo dia
        seen_dates: set[date] = set()

        plan_id = cast(int, p.id)
        for s in sessions_by_plan.get(plan_id, []):
            d = cast(date, s.performed_date)
            if d in seen_dates:
                continue
            seen_dates.add(d)

            if d.isoweekday() == plan_day_id:
                done_right += 1
            else:
                planned_day = planned_date_in_week(d, plan_day_id)
                if d < planned_day:
                    done_early += 1
                else:
                    done_wrong += 1

        done_total = done_right + done_early + done_wrong
        not_done = max(planned_total - done_total, 0)

        report.append(
            TrainingPlanReportItem(
                training_plan_id=plan_id,
                training_id=cast(int, p.training_id),
                day_id=plan_day_id,
                planned_total=planned_total,
                done_right_day=done_right,
                done_early=done_early,
                done_wrong_day=done_wrong,
                not_done=not_done,
            )
        )

    return report


@router.get("/exercise-progress/{training_plan_id}", response_model=list[ExerciseProgressReport])
def report_exercise_progress(
    training_plan_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    """
    Relatório de progresso dos exercícios de um plano de treino.
    Mostra estatísticas de cada exercício: quantas vezes executou, pulou,
    primeira e última execução, e progresso.
    """
    if start_date > end_date:
        raise HTTPException(400, "start_date não pode ser maior que end_date")

    # 1) Verificar se o plano existe
    training_plan = db.query(TrainingPlan).filter(TrainingPlan.id == training_plan_id).first()
    if not training_plan:
        raise HTTPException(404, "Plano de treino não encontrado")

    # 2) Buscar todos os exercícios do plano
    plan_exercises = (
        db.query(TrainingPlanExercise)
        .options(joinedload(TrainingPlanExercise.exercise))
        .filter(TrainingPlanExercise.training_plan_id == training_plan_id)
        .all()
    )

    if not plan_exercises:
        return []

    # 3) Buscar todas as sessões do plano no período
    sessions = (
        db.query(TrainingSession)
        .filter(
            TrainingSession.training_plan_id == training_plan_id,
            TrainingSession.performed_date.between(start_date, end_date),
        )
        .all()
    )

    total_sessions = len(sessions)
    session_ids = [cast(int, s.id) for s in sessions]

    # 4) Buscar todas as execuções dos exercícios nessas sessões
    if session_ids:
        executions = (
            db.query(TrainingExecution)
            .options(joinedload(TrainingExecution.training_session))
            .filter(TrainingExecution.training_session_id.in_(session_ids))
            .order_by(TrainingExecution.training_session_id)
            .all()
        )
    else:
        executions = []

    # 5) Organizar execuções por training_plan_exercise_id
    executions_by_exercise: dict[int, list[TrainingExecution]] = {}
    for ex in executions:
        plan_exercise_id = cast(int, ex.training_plan_exercise_id)
        executions_by_exercise.setdefault(plan_exercise_id, []).append(ex)

    # 6) Gerar relatório para cada exercício
    report: list[ExerciseProgressReport] = []

    for plan_ex in plan_exercises:
        plan_ex_id = cast(int, plan_ex.id)
        exercise = plan_ex.exercise
        exercise_id = cast(int, exercise.id)
        exercise_name = cast(str, exercise.name)
        exercise_type = cast(str, exercise.type)

        # Execuções deste exercício
        ex_list = executions_by_exercise.get(plan_ex_id, [])
        times_performed = len(ex_list)
        times_skipped = max(total_sessions - times_performed, 0)

        first_exec: ExerciseExecutionStats | None = None
        best_exec: ExerciseExecutionStats | None = None
        last_exec: ExerciseExecutionStats | None = None
        improvement_summary: str | None = None
        improvement_percentage: float | None = None

        if ex_list:
            # Ordenar por data (através do training_session.performed_date)
            sorted_execs = sorted(
                ex_list,
                key=lambda e: cast(date, e.training_session.performed_date)
            )

            # Primeira execução
            first = sorted_execs[0]
            first_exec = ExerciseExecutionStats(
                sets_done=first.sets_done,
                reps=first.reps,
                weight=first.weight,
                performed_date=str(cast(date, first.training_session.performed_date)),
            )

            # Última execução
            last = sorted_execs[-1]
            last_exec = ExerciseExecutionStats(
                sets_done=last.sets_done,
                reps=last.reps,
                weight=last.weight,
                performed_date=str(cast(date, last.training_session.performed_date)),
            )

            # Melhor execução (maior volume) - o recorde pessoal!
            best_execution = _find_best_execution(sorted_execs)
            if best_execution:
                best_exec = ExerciseExecutionStats(
                    sets_done=best_execution.sets_done,
                    reps=best_execution.reps,
                    weight=best_execution.weight,
                    performed_date=str(cast(date, best_execution.training_session.performed_date)),
                )

            # Gerar resumo de melhora e porcentagem baseado em médias
            if len(sorted_execs) > 1:
                # Calcular médias da primeira e segunda metade
                avg_first, avg_last = _calculate_average_executions(sorted_execs)

                if avg_first and avg_last:
                    improvement_summary = _generate_improvement_summary(avg_first, avg_last)
                    improvement_percentage = _calculate_improvement_percentage(avg_first, avg_last)

        report.append(
            ExerciseProgressReport(
                exercise_id=exercise_id,
                exercise_name=exercise_name,
                exercise_type=exercise_type,
                times_performed=times_performed,
                times_skipped=times_skipped,
                first_execution=first_exec,
                best_execution=best_exec,
                last_execution=last_exec,
                improvement_summary=improvement_summary,
                improvement_percentage=improvement_percentage,
            )
        )

    return report


def _generate_improvement_summary(
    first: ExerciseExecutionStats,
    last: ExerciseExecutionStats
) -> str:
    """Gera um resumo textual da evolução entre primeira e última execução"""
    parts = []

    # Comparar séries
    if first.sets_done and last.sets_done and first.sets_done != last.sets_done:
        diff = last.sets_done - first.sets_done
        if diff > 0:
            parts.append(f"+{diff} séries")
        else:
            parts.append(f"{diff} séries")

    # Comparar reps
    if first.reps and last.reps and first.reps != last.reps:
        diff = last.reps - first.reps
        if diff > 0:
            parts.append(f"+{diff} reps")
        else:
            parts.append(f"{diff} reps")

    # Comparar peso
    if first.weight and last.weight and first.weight != last.weight:
        diff = last.weight - first.weight
        if diff > 0:
            parts.append(f"+{diff}kg")
        else:
            parts.append(f"{diff}kg")

    if not parts:
        return "Sem mudanças significativas"

    return f"Evolução: {', '.join(parts)}"


def _calculate_improvement_percentage(
    first: ExerciseExecutionStats,
    last: ExerciseExecutionStats
) -> float | None:
    """
    Calcula a porcentagem de evolução baseada no volume total.
    Volume = séries × reps × peso

    Retorna:
    - Porcentagem positiva se melhorou
    - Porcentagem negativa se piorou
    - None se não houver dados suficientes para comparar
    """
    # Calcular volume da primeira execução
    first_volume = _calculate_volume(first)
    last_volume = _calculate_volume(last)

    # Se não tiver dados suficientes, retorna None
    if first_volume is None or first_volume == 0:
        return None

    if last_volume is None:
        return None

    # Calcular porcentagem de mudança
    # Fórmula: ((valor_final - valor_inicial) / valor_inicial) * 100
    percentage = ((last_volume - first_volume) / first_volume) * 100

    # Arredondar para 2 casas decimais
    return round(percentage, 2)


def _calculate_volume(stats: ExerciseExecutionStats) -> int | None:
    """
    Calcula o volume total de um exercício (séries × reps × peso).
    Retorna None se algum dado estiver faltando.
    """
    if stats.sets_done and stats.reps and stats.weight:
        return stats.sets_done * stats.reps * stats.weight

    # Se não tiver peso, considera apenas séries × reps
    if stats.sets_done and stats.reps:
        return stats.sets_done * stats.reps

    return None


def _find_best_execution(executions: list[TrainingExecution]) -> TrainingExecution | None:
    """
    Encontra a execução com o maior volume total (séries × reps × peso).
    Retorna None se não houver execuções válidas.
    """
    if not executions:
        return None

    best_exec = None
    best_volume = 0

    for ex in executions:
        # Calcular volume desta execução
        volume = 0
        sets = cast(int, ex.sets_done) if ex.sets_done is not None else 0
        reps = cast(int, ex.reps) if ex.reps is not None else 0
        weight = cast(int, ex.weight) if ex.weight is not None else 0

        if sets and reps and weight:
            volume = sets * reps * weight
        elif sets and reps:
            # Se não tiver peso, usa apenas sets × reps
            volume = sets * reps

        if volume > best_volume:
            best_volume = volume
            best_exec = ex

    return best_exec


def _calculate_average_executions(
    executions: list[TrainingExecution]
) -> tuple[ExerciseExecutionStats | None, ExerciseExecutionStats | None]:
    """
    Divide as execuções em duas metades e calcula a média de cada metade.

    Retorna:
    - (média_primeira_metade, média_segunda_metade)
    - (None, None) se não houver dados suficientes
    """
    if len(executions) < 2:
        return (None, None)

    # Dividir em duas metades
    mid_point = len(executions) // 2
    first_half = executions[:mid_point]
    second_half = executions[mid_point:]

    # Calcular média da primeira metade
    avg_first = _calculate_average_stats(first_half)

    # Calcular média da segunda metade
    avg_last = _calculate_average_stats(second_half)

    return (avg_first, avg_last)


def _calculate_average_stats(
    executions: list[TrainingExecution]
) -> ExerciseExecutionStats | None:
    """
    Calcula a média de séries, reps e peso de uma lista de execuções.
    """
    if not executions:
        return None

    # Filtrar execuções com dados válidos
    valid_sets = [cast(int, e.sets_done) for e in executions if e.sets_done is not None]
    valid_reps = [cast(int, e.reps) for e in executions if e.reps is not None]
    valid_weights = [cast(int, e.weight) for e in executions if e.weight is not None]

    # Calcular médias
    avg_sets = round(sum(valid_sets) / len(valid_sets)) if valid_sets else None
    avg_reps = round(sum(valid_reps) / len(valid_reps)) if valid_reps else None
    avg_weight = round(sum(valid_weights) / len(valid_weights)) if valid_weights else None

    # Pegar a data da última execução do grupo como referência
    last_exec = executions[-1]
    performed_date = str(cast(date, last_exec.training_session.performed_date))

    return ExerciseExecutionStats(
        sets_done=avg_sets,
        reps=avg_reps,
        weight=avg_weight,
        performed_date=performed_date,
    )


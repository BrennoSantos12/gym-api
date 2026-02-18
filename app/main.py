from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routers import auth_router, user_router, day_router, training_router, exercise_router, training_plan_router, training_plan_exercise_router, training_session_router, training_execution_router, report_router



app = FastAPI()


app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(day_router.router)
app.include_router(training_router.router)
app.include_router(exercise_router.router)
app.include_router(training_plan_router.router)
app.include_router(training_plan_exercise_router.router)
app.include_router(training_session_router.router)
app.include_router(training_execution_router.router)
app.include_router(report_router.router)

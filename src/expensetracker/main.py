from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from expensetracker.config import config
from expensetracker.routers.ExpenseController import router as ExpenseRouter
from expensetracker.routers.S3Controller import router as S3Router



app = FastAPI()

router = APIRouter()

@router.get("/")
def helloWorld():
    return "hello-world"



app.include_router(router)  
app.include_router(ExpenseRouter)
app.include_router(S3Router)
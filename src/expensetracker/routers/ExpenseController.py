from fastapi import APIRouter, HTTPException

from expensetracker.database.database import get_one_expense, insertNewExpense, deleteOneExpense, getAllExpenseNames
from expensetracker.models.Expense import ExpenseInsertRecord

router = APIRouter(prefix="/expenses")

@router.post("/")
def insertExpense(expense : ExpenseInsertRecord):
    try :
        return insertNewExpense(expense)
    except Exception as e :
        raise HTTPException(status_code=500, detail=f"{e}")
    

@router.get("/names")
def getExpenseNames():
    try:
        return getAllExpenseNames()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.get("/{item_id}")
def getExpenseById(item_id):
    try : 
        return get_one_expense(item_id)
    except Exception as e :
        raise HTTPException(status_code=500, detail=f"{e}")



@router.delete("/{item_id}")
def getExpenseById(item_id):
    try:
        return deleteOneExpense(item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
        



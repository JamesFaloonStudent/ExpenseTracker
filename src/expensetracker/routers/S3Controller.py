from fastapi import APIRouter, HTTPException

from expensetracker.database.s3 import create_upload_url, create_get_url
from expensetracker.models.s3Models import UploadRequest
from expensetracker.database.database import get_one_expense



router = APIRouter(prefix="/s3")


@router.post("/presignedUrl/upload")
def GetUploadPresignedUrl(req : UploadRequest):
    try :
        return create_upload_url(req)
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"{e}")


@router.get("/presignedUrl/get/{expense_id}")
def getRetrivePresignedUrl(expense_id : str):
    try :
        expense = get_one_expense(expense_id)
        return create_get_url(expense.s3ReceiptKey)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")






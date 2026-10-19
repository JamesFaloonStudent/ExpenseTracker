import os
import uuid
from dataclasses import asdict

from boto3 import resource

from expensetracker.models.Expense import Expense, ExpenseInsertRecord
from expensetracker.database.s3 import delete_image


REGION = os.environ['REGION']

expense_table = resource("dynamodb", region_name = REGION).Table("expenses")


def insertNewExpense(expense: ExpenseInsertRecord) -> str:
    item = asdict(expense)             # object -> dict
    item["id"] = str(uuid.uuid4())  



    try:
        expense_table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(id)", 
        )
        return item["id"]
    except Exception as e:
        print(f"failure occurred at insert function: {e}")
        raise




def get_one_expense(expense_id: str) -> Expense | None:
    try:
        response = expense_table.get_item(Key={"id": expense_id})
        print(response)
        item = response.get("Item")
        print(item)
        return Expense(
            id=item["id"],
            name=item["name"],
            s3ReceiptKey=item.get("s3ReceiptKey"),  # None if missing
            value=float(item["value"]),                   # Decimal -> float
        )
    except Exception as e:
        print(f"failure occurred at get_one function: {e}")
        raise




def deleteOneExpense(expense_id : str):
    try :
        item_detials = get_one_expense(expense_id)
        delete_image(item_detials.s3ReceiptKey)
        response = expense_table.delete_item(Key={"id" : expense_id})
        return response
    except Exception as e :
        raise


def getAllExpenseNames() -> list[str]:
    names = []
    keywordArgs = {
        "ProjectionExpression": "#n",
        "ExpressionAttributeNames": {"#n": "name"},
    }
    try:
        while True:
            response = expense_table.scan(**keywordArgs)
            names.extend(item["name"] for item in response.get("Items", []) if "name" in item)

            last_key = response.get("LastEvaluatedKey")
            if not last_key:
                break
            keywordArgs["ExclusiveStartKey"] = last_key
        return names
    except Exception as e:
        print(f"failure occurred at get_all_expense_names: {e}")
        raise



    
    
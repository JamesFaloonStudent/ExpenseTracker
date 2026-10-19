from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExpenseInsertRecord:
    name : str
    s3ReceiptKey : str
    value : Decimal

@dataclass
class Expense:
    id : str
    name : str
    s3ReceiptKey : str
    value : Decimal
    


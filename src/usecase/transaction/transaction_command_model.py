from pydantic import BaseModel


class TransactionCreateModel(BaseModel):
    account_id: str
    amount: float
    transaction_type: str

from pydantic import BaseModel, Field

from src.domain.transaction import Transaction


class TransactionReadModel(BaseModel):
    """TransactionReadModel represents data structure as a read model."""

    account_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    amount: float
    transaction_type: str

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(transaction: Transaction) -> "TransactionReadModel":
        return TransactionReadModel(
            account_id=transaction.account_id,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type,
        )

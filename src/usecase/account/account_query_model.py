from pydantic import BaseModel, Field

from src.domain.account import Account


class AccountReadModel(BaseModel):
    """AccountReadModel represents data structure as a read model."""

    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    customer_id: str
    account_number: str
    balance: float

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(account: Account) -> "AccountReadModel":
        return AccountReadModel(
            id=account.account_id,
            customer_id=account.customer_id,
            account_number=account.account_number,
            balance=account.balance,
        )

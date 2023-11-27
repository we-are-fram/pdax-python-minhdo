from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.account import Account
from src.infrastructure.sqlite.database import Base
from src.usecase.account import AccountReadModel


class AccountDTO(Base):
    """AccountDTO is a data transfer object associated with Account entity."""

    __tablename__ = "account"
    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    account_number: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    customer_id: Mapped[str] = mapped_column(nullable=False)
    balance: Mapped[float] = mapped_column(nullable=True)

    def to_entity(self) -> Account:
        return Account(
            account_id=self.id,
            account_number=self.account_number,
            customer_id=self.customer_id,
            balance=self.balance,
        )

    def to_read_model(self) -> AccountReadModel:
        return AccountReadModel(
            id=self.id,
            account_number=self.account_number,
            customer_id=self.customer_id,
            balance=self.balance,
        )

    @staticmethod
    def from_entity(account: Account) -> "AccountDTO":
        return AccountDTO(
            id=account.account_id,
            account_number=account.account_number,
            customer_id=account.customer_id,
            balance=account.balance,
        )

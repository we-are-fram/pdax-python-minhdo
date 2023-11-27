from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.transaction import Transaction
from src.infrastructure.sqlite.database import Base
from src.usecase.transaction import TransactionReadModel


class TransactionDTO(Base):
    """TransactionDTO is a data transfer object associated with Account entity."""

    __tablename__ = "transaction"
    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    account_id: Mapped[str] = mapped_column(String(17), nullable=False)
    transaction_type: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)

    def to_entity(self) -> Transaction:
        return Transaction(
            transaction_id=self.id,
            account_id=self.account_id,
            amount=self.amount,
            transaction_type=self.transaction_type,
        )

    def to_read_model(self) -> TransactionReadModel:
        return TransactionReadModel(
            id=self.id,
            amount=self.amount,
            account_id=self.account_id,
            transaction_type=self.transaction_type,
        )

    @staticmethod
    def from_entity(transaction: Transaction) -> "TransactionDTO":
        return TransactionDTO(
            id=transaction.transaction_id,
            account_id=transaction.account_id,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type,
        )

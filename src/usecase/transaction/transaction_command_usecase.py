from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid

from src.domain.account import Account
from src.domain.transaction import (
    Transaction,
    TransactionRepository,
)
from src.usecase.account.account_query_model import AccountReadModel
from .transaction_command_model import TransactionCreateModel


class TransactionCommandUseCaseUnitOfWork(ABC):
    """TransactionCommandUseCaseUnitOfWork defines an interface based on Unit of Work pattern."""

    transaction_repository: TransactionRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class TransactionCommandUseCase(ABC):
    """TransactionCommandUseCase defines a command use case interface related Transaction entity."""

    @abstractmethod
    def create_transaction(self, data: TransactionCreateModel) -> Optional[TransactionCreateModel]:
        raise NotImplementedError


class TransactionCommandUseCaseImpl(TransactionCommandUseCase):
    """TransactionCommandUseCaseImpl implements a command usecases related Transaction entity."""

    def __init__(
            self,
            uow: TransactionCommandUseCaseUnitOfWork,
            account_uow
    ):
        self.uow: TransactionCommandUseCaseUnitOfWork = uow
        self.account_uow = account_uow

    def create_transaction(self, data: TransactionCreateModel):
        try:
            uuid = shortuuid.uuid()
            transaction = Transaction(
                transaction_id=uuid,
                account_id=data.account_id,
                amount=data.amount,
                transaction_type=data.transaction_type
            )

            self.uow.transaction_repository.create(transaction)
            self.uow.commit()

        except Exception as e:
            print(str(e))
            self.uow.rollback()
            raise

        existing_account = self.account_uow.account_repository.find_by_id(data.account_id)
        balance = existing_account.get_balance(data.amount, data.transaction_type)
        self.account_uow.account_repository.partial_update(data.account_id, balance=balance)
        self.account_uow.commit()
        AccountReadModel.from_entity(cast(Account, existing_account))
        return AccountReadModel.from_entity(cast(Account, existing_account))

from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid

from src.domain.account import (
    Account,
    AccountRepository,
)
from .account_command_model import AccountCreateModel
from .account_query_model import AccountReadModel


class AccountCommandUseCaseUnitOfWork(ABC):
    """AccountCommandUseCaseUnitOfWork defines an interface based on Unit of Work pattern."""

    account_repository: AccountRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class AccountCommandUseCase(ABC):
    """AccountCommandUseCase defines a command usecase inteface related Account entity."""

    @abstractmethod
    def create_account(self, data: AccountCreateModel) -> Optional[AccountCreateModel]:
        raise NotImplementedError


class AccountCommandUseCaseImpl(AccountCommandUseCase):
    """AccountCommandUseCaseImpl implements a command usecases related Account entity."""

    def __init__(
            self,
            uow: AccountCommandUseCaseUnitOfWork,
    ):
        self.uow: AccountCommandUseCaseUnitOfWork = uow

    def create_account(self, data: AccountCreateModel) -> Optional[AccountReadModel]:
        try:
            customer_id = data.customer_id
            uuid = shortuuid.uuid()
            account = Account(account_id=uuid,
                              account_number=uuid,
                              customer_id=customer_id)

            self.uow.account_repository.create(account)
            self.uow.commit()

            created_account = self.uow.account_repository.find_by_id(uuid)
        except Exception as e:
            print(str(e))
            self.uow.rollback()
            raise

        return AccountReadModel.from_entity(cast(Account, created_account))

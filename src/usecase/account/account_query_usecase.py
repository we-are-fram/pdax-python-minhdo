from abc import ABC, abstractmethod
from typing import List, Optional

from .account_query_model import AccountReadModel
from .account_query_service import AccountQueryService


class AccountQueryUseCase(ABC):
    """AccountQueryUseCase defines a query usecase inteface related Account entity."""

    @abstractmethod
    def fetch_account_by_id(self, account_id: str) -> Optional[AccountReadModel]:
        """fetch_account_by_id fetches a account by id."""
        raise NotImplementedError

    @abstractmethod
    def fetch_accounts(self) -> List[AccountReadModel]:
        """fetch_accounts fetches accounts."""
        raise NotImplementedError

    @abstractmethod
    def fetch_accounts_by_customer_id(self, customer_id: str) -> List[AccountReadModel]:
        """fetch_accounts fetches accounts by using the customer_id."""
        raise NotImplementedError


class AccountQueryUseCaseImpl(AccountQueryUseCase):
    """AccountQueryUseCaseImpl implements a query usecases related Account entity."""

    def __init__(self, account_query_service: AccountQueryService):
        self.account_query_service: AccountQueryService = account_query_service

    def fetch_account_by_id(self, account_id: str) -> Optional[AccountReadModel]:
        """fetch_account_by_id fetches a account by id."""
        try:
            account = self.account_query_service.find_by_id(account_id)
            if account is None:
                raise Exception
        except Exception as e:
            print(str(e))
            raise

        return account

    def fetch_accounts(self) -> List[AccountReadModel]:
        """fetch_accounts fetches accounts."""
        try:
            accounts = self.account_query_service.find_all()
        except Exception as e:
            print(str(e))
            raise

        return accounts

    def fetch_accounts_by_customer_id(self, customer_id: str):
        try:
            accounts = self.account_query_service.find_accounts_by_customer_id(customer_id)
        except Exception as e:
            print(str(e))
            raise

        return accounts

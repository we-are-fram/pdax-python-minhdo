from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from src.domain.account import Account, AccountRepository
from src.usecase.account import AccountCommandUseCaseUnitOfWork
from .account_dto import AccountDTO


class AccountRepositoryImpl(AccountRepository):
    """AccountRepositoryImpl implements CRUD operations related Account entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, account_id: str) -> Optional[Account]:
        try:
            account_dto = self.session.query(AccountDTO).filter_by(id=account_id).one()
        except NoResultFound:
            return None
        except Exception as e:
            print(str(e))
            raise

        return account_dto.to_entity()

    def find_by_customer_id(self, customer_id: str) -> Optional[Account]:
        account_dto = self.session.query(AccountDTO).filter_by(customer_id=customer_id).one()
        return account_dto.to_entity()

    def create(self, account: Account):
        account_dto = AccountDTO.from_entity(account)
        try:
            self.session.add(account_dto)
        except Exception as e:
            print(str(e))
            raise

    def partial_update(self, account_id: str, **kwargs):
        account = self.session.query(AccountDTO).filter_by(id=account_id).one()
        if kwargs:
            for k, v in kwargs.items():
                setattr(account, k, v)

    def delete_by_id(self, account_id: str):
        try:
            self.session.query(AccountDTO).filter_by(id=account_id).delete()
        except Exception as e:
            print(str(e))
            raise


class AccountCommandUseCaseUnitOfWorkImpl(AccountCommandUseCaseUnitOfWork):
    def __init__(
            self,
            session: Session,
            account_repository: AccountRepository,
    ):
        self.session: Session = session
        self.account_repository: AccountRepository = account_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

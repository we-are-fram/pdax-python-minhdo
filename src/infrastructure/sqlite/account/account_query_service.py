from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from src.usecase.account import AccountQueryService, AccountReadModel
from .account_dto import AccountDTO


class AccountQueryServiceImpl(AccountQueryService):
    """AccountQueryServiceImpl implements READ operations related Account entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[AccountReadModel]:
        try:
            account_dto = self.session.query(AccountDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except Exception as e:
            print(str(e))
            raise

        return account_dto.to_read_model()

    def find_all(self) -> List[AccountReadModel]:
        try:
            account_dtos = (
                self.session.query(AccountDTO)
                .limit(100)
                .all()
            )
        except Exception as e:
            print(str(e))
            raise

        if len(account_dtos) == 0:
            return []

        return list(map(lambda account_dto: account_dto.to_read_model(), account_dtos))

    def find_accounts_by_customer_id(self, customer_id: str) -> List[AccountReadModel]:
        try:
            account_dtos = (
                self.session.query(AccountDTO).filter_by(customer_id=customer_id).one()
                .limit(100)
                .all()
            )
        except Exception as e:
            print(str(e))
            raise

        if len(account_dtos) == 0:
            return []

        return list(map(lambda account_dto: account_dto.to_read_model(), account_dtos))

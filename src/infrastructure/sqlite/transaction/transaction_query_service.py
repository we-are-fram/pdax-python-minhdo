from typing import List

from sqlalchemy.orm.session import Session

from src.usecase.transaction import TransactionQueryService, TransactionReadModel
from .transaction_dto import TransactionDTO


class TransactionQueryServiceImpl(TransactionQueryService):
    """AccountQueryServiceImpl implements READ operations related Transaction entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def fetch_transactions_by_account_id(self, account_id: str) -> List[TransactionReadModel]:
        try:
            transaction_dtos = (
                self.session.query(TransactionDTO).filter_by(account_id=account_id)
                .all()
            )
        except Exception as e:
            print(str(e))
            raise

        if len(transaction_dtos) == 0:
            return []

        return list(map(lambda transaction_dto: transaction_dto.to_read_model(), transaction_dtos))

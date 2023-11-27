from sqlalchemy.orm.session import Session

from src.domain.transaction import TransactionRepository, Transaction
from src.usecase.transaction import TransactionCommandUseCaseUnitOfWork
from .transaction_dto import TransactionDTO


class TransactionRepositoryImpl(TransactionRepository):
    """AccountRepositoryImpl implements CRUD operations related Account entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, transaction: Transaction):
        transaction_dto = TransactionDTO.from_entity(transaction)
        try:
            self.session.add(transaction_dto)
        except Exception as e:
            print(str(e))
            raise
        pass

    def find_by_id(self, transaction_id: str):
        pass


class TransactionCommandUseCaseUnitOfWorkImpl(TransactionCommandUseCaseUnitOfWork):
    def __init__(
            self,
            session: Session,
            transaction_repository: TransactionRepository,
    ):
        self.session: Session = session
        self.transaction_repository: TransactionRepository = transaction_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

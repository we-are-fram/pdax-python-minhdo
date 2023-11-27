import logging
from logging import config
from typing import Iterator

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src.domain.account import *
from src.domain.transaction import *
from src.infrastructure.sqlite.account import (
    AccountCommandUseCaseUnitOfWorkImpl,
    AccountQueryServiceImpl,
    AccountRepositoryImpl,
)
from src.infrastructure.sqlite.database import SessionLocal, create_tables
from src.infrastructure.sqlite.transaction import (
    TransactionCommandUseCaseUnitOfWorkImpl,
    TransactionQueryServiceImpl,
    TransactionRepositoryImpl,
)
#############
from src.usecase.account import *
from src.usecase.transaction import *

#############

config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

create_tables()


def get_session() -> Iterator[Session]:
    """Get a session from the database."""
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


####################
####################

def account_query_usecase(session: Session = Depends(get_session)) -> AccountQueryUseCase:
    account_query_service: AccountQueryService = AccountQueryServiceImpl(session)
    return AccountQueryUseCaseImpl(account_query_service)


def account_command_usecase(session: Session = Depends(get_session)) -> AccountCommandUseCase:
    account_repository: AccountRepository = AccountRepositoryImpl(session)
    uow: AccountCommandUseCaseUnitOfWork = AccountCommandUseCaseUnitOfWorkImpl(
        session, account_repository=account_repository
    )
    return AccountCommandUseCaseImpl(uow)


@app.post(
    "/accounts",
    response_model=AccountReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": {},
        },
    },
)
async def create_account(
        data: AccountCreateModel,
        account_command_usecase: AccountCommandUseCase = Depends(account_command_usecase),
):
    try:
        account = account_command_usecase.create_account(data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return account


def transaction_query_usecase(session: Session = Depends(get_session)) -> TransactionQueryUseCase:
    transaction_query_service: TransactionQueryService = TransactionQueryServiceImpl(session)
    return TransactionQueryUseCaseImpl(transaction_query_service)


def transaction_command_usecase(session: Session = Depends(get_session)) -> TransactionCommandUseCase:
    transaction_repository: TransactionRepository = TransactionRepositoryImpl(session)
    account_repository: AccountRepository = AccountRepositoryImpl(session)
    uow: TransactionCommandUseCaseUnitOfWork = TransactionCommandUseCaseUnitOfWorkImpl(
        session, transaction_repository=transaction_repository
    )
    account_uow: AccountCommandUseCaseUnitOfWork = AccountCommandUseCaseUnitOfWorkImpl(
        session, account_repository=account_repository
    )
    return TransactionCommandUseCaseImpl(uow, account_uow)


@app.post(
    "/transactions",
    response_model=AccountReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": {},
        },
    },
)
async def make_transaction(
        data: TransactionCreateModel,
        transaction_command_usecase: TransactionCommandUseCase = Depends(transaction_command_usecase),
):
    try:
        transaction = transaction_command_usecase.create_transaction(data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return transaction


@app.get(
    "/accounts/{account_id}/statements",
    response_model=[],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": {},
        },
    },
)
async def gen_account_statements(
        account_id: str,
        transaction_query_usecase: TransactionQueryUseCase = Depends(transaction_query_usecase),
):
    try:
        transactions = transaction_query_usecase.fetch_transactions_by_account_id(account_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return transactions

####################
####################

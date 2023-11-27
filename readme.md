## Code Architecture


```tree
├── main.py
├── src
│   ├── domain
│   │   └── account
|   |   |__ transaction
│   ├── infrastructure
│   │   └── sqlite
│   │       ├── account
│   │       ├── transaction
│   │       └── database.py
│   └── usecase
│       └── account
│       └── transaction
└── tests
    \_ not done yet
```


```

### Entity

To represent an Domain - Entity in Python.

- [account.py](./src/domain/account/account.py)

```python
class Account:
    def __init__(
        self,
        account_id: str,
        customer_id: str,
        account_number: str,
        balance: float = 0.0,
    ):
        self.account_id: str = account_id
        self.customer_id: str = customer_id
        self.account_number: str = account_number
        self.balance: float = balance
    
    def ...
    
    def ...
```

### DTO (Data Transfer Object)

DTO (Data Transfer Object).

The domain layer would be dependent on the outer layer.

Two rules:

1. Domain layer --DO NOT-- extend SQLAlchemy Base class.
2. Data transfer Objects extend the mapper class.
   -[account_dto.py](./src/infrastructure/sqlite/account/account_dto.py)
   -[transaction_dto.py](./src/infrastructure/sqlite/transaction/transaction_dto.py)


### CQRS

- Read model and Write model
  1. Define read models and write models in the --use case layer--
    - Account
      -[account_query_model.py](./src/usecase/account/account_query_model.py)
      -[account_command_model.py](./src/usecase/account/account_command_model.py)
    - Transaction
      -[transaction_query_model.py](./src/usecase/account/account_query_model.py)
      -[transaction_command_model.py](./src/usecase/account/account_command_model.py)
- Query
  1. Query service in the --use case layer--
     - [account_query_service.py (interface)](./src/usecase/account/account_query_service.py)
     - [transaction_query_service.py (interface)](./src/usecase/transaction/transaction_query_service.py)
  2. Query service in the --infrastructure layer--
     - [account_query_service.py](./src/infrastructure/sqlite/account/account_query_service.py)
     - [transaction_query_service.py](./src/infrastructure/sqlite/transaction/transaction_query_service.py)
- Command
  1. Repository interfaces in the --domain layer--
     - [account_repository.py (interface)](./src/domain/account/account_repository.py)
     - [transaction_repository.py (interface)](./src/domain/transaction/transaction_repository.py)
  2. Repository in the --infrastructure layer--
     - [account_repository.py](./src/infrastructure/sqlite/account/account_repository.py)
     - [transaction_repository.py](./src/infrastructure/sqlite/transaction/transaction_repository.py)
- Use case
  1. Usecases based on repository interfaces or query service interfaces.
    - Account
      - [account_query_usecase.py](./src/usecase/account/account_query_usecase.py)
      - [account_command_usecase.py](./src/usecase/account/account_command_usecase.py)
    - Transaction
      - [transaction_query_usecase.py](./src/usecase/transaction/transaction_query_usecase.py)
      - [transaction_command_usecase.py](./src/usecase/transaction/transaction_command_usecase.py)
  2. Usecases return an instance of read|write model to a main routine.



### UoW (Unit of Work)

Isolating the domain layer

UoW (Unit of Work)

Interface base on UoW  in the use case layer.

- [account_command_usecase.py](./src/usecase/account/account_command_usecase.py)

```python
class AccountCommandUseCaseUnitOfWork(ABC):
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

```

Infrastructure layer using the above interface.

-[account_repository.py](./src/infrastructure/sqlite/account/account_repository.py)

```python
class AccountCommandUseCaseUnitOfWorkImpl(AcountCommandUseCaseUnitOfWork):
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
```

`session` <- SQLAlchemy,


## How to work
1. Install python via pyenv or virtualenv
2. Run `uvicorn main:app --host 0.0.0.0 --port 80` on the local machine
3. Access the API document http://0.0.0.0:80/docs
4. Follow the swagger ![swagger.png](images%2Fswagger.png)
5. We can drop db DB by deleting [sqlite.db](db%2Fsqlite.db)

## Summarize
- Mainly focus on class, infrastructure design. Implement code following the best case only
- Dont have enough time for the unit test


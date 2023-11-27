from pydantic import BaseModel


class AccountCreateModel(BaseModel):
    """AccountCreateModel represents a write model to create a account."""
    customer_id: str
    name: str
    email: str
    phone_number: str

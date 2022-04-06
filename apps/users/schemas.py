import typing as t

from pydantic import BaseModel, Field

from utils.enums import Status


class User(BaseModel):
    id: int = Field(gt=0)
    first_name: str = Field(min_length=1, max_length=200)
    last_name: str = Field(max_length=200)
    patr_name: str = Field(max_length=200)

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=200)
    last_name: str = Field(max_length=200)
    patr_name: str = Field(max_length=200)


class BalanceOut(BaseModel):
    user_id: int
    balance: float
    currency: str = 'RUR'


class UserResponse(BaseModel):
    status: Status
    description: str = ''
    user: t.Optional[User] = None

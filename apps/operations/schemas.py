import datetime
import typing as t

from pydantic import BaseModel, root_validator, Field
from utils.enums import OperationType, Status


class Operation(BaseModel):
    type: OperationType
    amount: float = Field(gt=0)
    user_from_id: t.Optional[int] = None
    user_to_id: t.Optional[int] = None
    comment: str = Field(str(), max_length=500)

    class Config:
        orm_mode = True


class OneUserOperation(Operation):
    @root_validator
    def type_based_validation(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        if values.get('type') == OperationType.withdrawal:
            assert values.get('user_from_id') > 0, f"user_from_id must be filled."
            values['user_to_id'] = None
        elif values.get('type') == OperationType.accrual:
            assert values.get('user_to_id') > 0, f"user_to_id must be filled."
            values['user_from_id'] = None
        return values


class TwoUserOperation(Operation):
    user_from_id: int = Field(gt=0)
    user_to_id: int = Field(gt=0)

    @root_validator
    def users_validation(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        assert values.get('user_from_id') != values.get('user_to_id'), "users must be different."
        return values


class Withdrawal(OneUserOperation):
    @root_validator(pre=True)
    def set_type(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        values['type'] = OperationType.withdrawal
        return values


class Accrual(OneUserOperation):
    @root_validator(pre=True)
    def set_type(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        values['type'] = OperationType.accrual
        return values


class Transaction(TwoUserOperation):
    @root_validator(pre=True)
    def set_type(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        values['type'] = OperationType.transaction
        return values


class OperationResponse(BaseModel):
    status: Status
    description: str = ''


class HistoryFilter(BaseModel):
    user_id: int = Field(gt=0)
    date_from: t.Optional[datetime.date] = None
    date_to: t.Optional[datetime.date] = None
    amount_gt: t.Optional[float] = None
    amount_lt: t.Optional[float] = None

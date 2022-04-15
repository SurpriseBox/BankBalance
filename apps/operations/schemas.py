import datetime
import typing as t
from decimal import Decimal

from pydantic import BaseModel, root_validator, Field

from utils.enums import OperationType, Status, OperationStatus


class Operation(BaseModel):
    type: OperationType
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=4)
    user_from_id: t.Optional[int] = None
    user_to_id: t.Optional[int] = None
    comment: str = Field(str(), max_length=500)

    class Config:
        orm_mode = True


class OperationOut(Operation):
    status: OperationStatus
    timestamp: datetime.datetime

    class Config:
        orm_mode = True


class OneUserOperation(Operation):
    @root_validator
    def type_based_validation(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """

        :param values:
        :return:
        """
        if values.get('type') == OperationType.withdrawal:
            if not values.get('user_from_id'):
                raise ValueError(f"user_from_id must be filled.")
            values['user_to_id'] = None
        elif values.get('type') == OperationType.accrual:
            if not values.get('user_to_id'):
                raise ValueError(f"user_to_id must be filled.")
            values['user_from_id'] = None
        return values


class TwoUserOperation(Operation):
    user_from_id: int = Field(gt=0)
    user_to_id: int = Field(gt=0)

    @root_validator
    def users_validation(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """

        :param values:
        :return:
        """
        if values.get('user_from_id') == values.get('user_to_id'):
            raise ValueError("users must be different.")
        return values


class Withdrawal(OneUserOperation):
    @root_validator(pre=True)
    def set_type(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """

        :param values:
        :return:
        """
        values['type'] = OperationType.withdrawal
        return values


class Accrual(OneUserOperation):
    @root_validator(pre=True)
    def set_type(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """

        :param values:
        :return:
        """
        values['type'] = OperationType.accrual
        return values


class Transaction(TwoUserOperation):
    @root_validator(pre=True)
    def set_type(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """

        :param values:
        :return:
        """
        values['type'] = OperationType.transaction
        return values


class OperationResponse(BaseModel):
    status: Status
    operation_status: OperationStatus
    description: str = ''


class HistoryFilter(BaseModel):
    user_id: int = Field(gt=0)
    date_from: t.Optional[datetime.date] = None
    date_to: t.Optional[datetime.date] = None
    amount_gt: t.Optional[float] = None
    amount_lt: t.Optional[float] = None

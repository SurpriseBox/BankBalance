import typing as t
from enum import Enum


class OperationType(Enum):
    withdrawal = 'withdrawal'
    accrual = 'accrual'
    transaction = 'transaction'


class OneUserOperationType(Enum):
    withdrawal = 'withdrawal'
    accrual = 'accrual'


class TwoUserOperationType(Enum):
    transaction = 'transaction'


class Status(Enum):
    success = 'success'
    error = 'error'
    db_error = 'database_error'
    data_error = 'data_error'


OperationNeedBalanceCheck: t.Dict[OperationType, bool] = {
    OperationType.withdrawal: True,
    OperationType.accrual: False,
    OperationType.transaction: True
}

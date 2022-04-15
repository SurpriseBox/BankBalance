
import typing as t
from enum import Enum


class OperationType(str, Enum):
    withdrawal = 'withdrawal'
    accrual = 'accrual'
    transaction = 'transaction'


class OneUserOperationType(str, Enum):
    withdrawal = 'withdrawal'
    accrual = 'accrual'


class TwoUserOperationType(str, Enum):
    transaction = 'transaction'


class Status(str, Enum):
    success = 'success'
    error = 'error'
    db_error = 'database_error'
    data_error = 'data_error'


class OperationStatus(str, Enum):
    created = 'Created'
    pending = 'Pending'
    in_progress = 'In Progress'
    success = 'Success'
    error = 'Error'


OperationNeedBalanceCheck: t.Dict[OperationType, bool] = {
    OperationType.withdrawal: True,
    OperationType.accrual: False,
    OperationType.transaction: True
}


OperationStatusChangeChain: t.Dict[OperationStatus, t.Tuple[OperationStatus]] = {
    OperationStatus.created: (OperationStatus.pending, ),
    OperationStatus.pending: (OperationStatus.in_progress, ),
    OperationStatus.in_progress: (OperationStatus.success, OperationStatus.error)
}

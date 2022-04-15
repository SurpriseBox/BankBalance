
from decimal import Decimal

from db.models import Operation
from .enums import OperationStatus


class OperationStatusChangeException(Exception):
    """

    """
    def __init__(self, operation: Operation, wrong_status: OperationStatus):
        self._wrong_status = wrong_status
        self._op = operation

    def __str__(self):
        return f"Wrong operation status change: {self._op}, from {self._op.status} to {self._wrong_status}."


class ObjectNotFoundException(Exception):
    """

    """
    def __init__(self, obj_type: type, obj_id: int):
        self._type = obj_type
        self._id = obj_id

    def __str__(self):
        return f"{self._type.__name__} with id={self._id} not found."


class LowUserBalanceException(Exception):
    """

    """
    def __init__(self, user_id: int, wrong_amount: Decimal):
        self._user_id = user_id
        self._wrong_amount = wrong_amount

    def __str__(self):
        return f"user(id={self._user_id}) lower than {self._wrong_amount}"


class MQServerConnectionError(Exception):
    """

    """
    def __init__(self, url: str, message: str):
        self._url = url
        self._message = message

    def __str__(self):
        return f"Connection to MQ on {self._url} failed. Reason: {self._message}"


class TransactionRequiredException(Exception):
    """

    """
    def __str__(self):
        return "You need to start transaction before using this function."


import datetime
import typing as t
from decimal import Decimal
from math import inf

import sqlalchemy.sql.expression as sql_expr
from deprecation import deprecated
from pydantic import BaseModel
from sqlalchemy import DATE
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import select

import apps.users.schemas as user_schemas
from utils.decorators import transaction_required, transaction_if_needed
from utils.enums import OperationType, OperationStatus, OperationStatusChangeChain
from utils.exceptions import OperationStatusChangeException, ObjectNotFoundException, LowUserBalanceException
from .models import Operation, User


# Common CRUD
@transaction_required
async def add(session: AsyncSession, model: t.Type, instance: BaseModel, **additional_attributes) -> t.Any:
    d_ = {**instance.dict(), **additional_attributes}
    new_instance: model = model(**d_)
    session.add(new_instance)
    return new_instance


@transaction_if_needed
async def get(session: AsyncSession, model: t.Type, instance_id: int) -> t.Any:
    result = await session.execute(select(model).where(model.id == instance_id))
    instance = result.scalars().one_or_none()
    if not instance:
        raise ObjectNotFoundException(model, instance_id)
    return instance


@transaction_if_needed
async def get_list(session: AsyncSession, model: t.Type) -> t.List[t.Type]:
    result = await session.execute(select(model).options(selectinload()))
    instance_list = result.scalars().all()
    return instance_list


# User CRUD
@deprecated(details='use db.crud.add(session, model, instance) instead.')
@transaction_required
async def add_user(session: AsyncSession, user: user_schemas.UserCreate) -> User:
    """

    :param session:
    :param user:
    :return:
    """
    new_instance: User = User(**user.dict())
    session.add(new_instance)
    return new_instance


@deprecated(details='use db.crud.get(session, model, instance_id) instead.')
@transaction_if_needed
async def get_user(session: AsyncSession, user_id: int) -> User:
    """

    :param session:
    :param user_id:
    :return:
    """
    statement = select(User).where(User.id == user_id)
    user: User = await session.execute(statement).scalars().one()
    if not user:
        raise ObjectNotFoundException(User, user_id)
    return user


@deprecated(details='use db.crud.get_list(session, model) instead.')
@transaction_if_needed
async def get_users_list(session: AsyncSession) -> t.List[User]:
    statement = select(User)
    model_list = await session.execute(statement).scalars().all()
    return model_list


@transaction_if_needed
async def get_balance(session: AsyncSession, user_id: int) -> Decimal:
    """

    :param session:
    :param user_id:
    :return:
    """
    user: User = await get(session, User, user_id)
    return user.balance


@transaction_required
async def change_balance(session: AsyncSession, user_id: int, amount: Decimal):
    user: User = await get(session, User, user_id)
    if amount < 0 and user.balance < amount.copy_abs():
        raise LowUserBalanceException(user_id, amount.copy_abs())
    user.balance += amount
    print(f"new user {user_id} balance = {user.balance}")
    session.add(user)
    return user


# Operation CRUD
@deprecated(details='use db.crud.add(session, model, instance) instead.')
@transaction_required
async def add_operation(session: AsyncSession, operation) -> Operation:
    """

    :param session:
    :param operation:
    :return:
    """
    new_operation = Operation(**operation.dict(), timestamp=datetime.datetime.now())
    session.add(new_operation)
    return new_operation


@deprecated(details='use db.crud.get(session, model, instance_id) instead.')
@transaction_if_needed
async def get_operation(session: AsyncSession, operation_id: int) -> Operation:
    """

    :param session:
    :param operation_id:
    :return:
    """
    result = await session.execute(select(Operation).where(Operation.id == operation_id))
    operation: Operation = result.scalars().one_or_none()
    if not operation:
        raise ObjectNotFoundException(Operation, operation_id)
    return operation


@deprecated(details='use db.crud.get_list(session, model) instead.')
@transaction_if_needed
async def get_operations_list(session: AsyncSession) -> t.List[Operation]:
    """

    :param session:
    :return:
    """
    result = await session.execute(select(Operation).options(selectinload()))
    operations: t.List[Operation] = result.scalars().all()
    return operations


@transaction_required
async def change_operation_status(
        session: AsyncSession,
        operation_id: int,
        new_status: OperationStatus
):
    """
    Change operation status.
    Checks if new_status is allowed, raises OperationStatusChangeException if it doesn't.

    :param session:
    :param operation_id:
    :param new_status:
    """
    operation: Operation = await get(session, Operation, operation_id)

    if new_status not in OperationStatusChangeChain.get(operation.status):
        raise OperationStatusChangeException(operation, new_status)

    operation.status = new_status
    session.add(operation)


@transaction_if_needed
async def get_history(
        session: AsyncSession,
        user_id: int,
        amount_gt: float = 0,
        amount_lt: float = inf,
        date_from: datetime.date = None,
        date_to: datetime.date = None
) -> t.List[Operation]:
    """

    :param session:
    :param user_id:
    :param amount_gt:
    :param amount_lt:
    :param date_from:
    :param date_to:
    :return:
    """
    filter_ = [
        sql_expr.or_(sql_expr.and_(Operation.type.in_([OperationType.transaction, OperationType.withdrawal]),
                                   Operation.user_from_id == user_id),
                     sql_expr.and_(Operation.type.in_([OperationType.transaction, OperationType.accrual]),
                                   Operation.user_to_id == user_id))
    ]
    if amount_gt:
        filter_.append(Operation.amount >= amount_gt)
    if amount_lt:
        filter_.append(Operation.amount <= amount_lt)
    if date_from:
        filter_.append(sql_expr.cast(Operation.timestamp, DATE) >= date_from)
    if date_to:
        filter_.append(sql_expr.cast(Operation.timestamp, DATE) <= date_to)

    result = await session.execute(select(Operation).where(*filter_))
    operations: t.List[Operation] = result.scalars().all()
    return operations

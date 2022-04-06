
import datetime
import typing as t

from sqlalchemy.orm.session import Session
import sqlalchemy.sql.expression as sql_expr
from sqlalchemy import DATE

import apps.operations.schemas as op_schemas
import apps.users.schemas as u_schemas
from utils.enums import OperationType
from .models import Operation, User
from math import inf


async def add_user(s: Session, user: u_schemas.UserCreate) -> User:
    o = User(**user.dict())
    s.add(o)
    s.commit()
    return o


async def get_user(s: Session, user_id: int) -> User:
    return s.query(User).filter(User.id == user_id).first()


async def get_users_list(s: Session) -> t.List[User]:
    return s.query(User).all()


async def get_balance(s: Session, user_id: int) -> float:
    in_ = s.query(Operation).filter(Operation.user_to_id == user_id).all()
    out_ = s.query(Operation).filter(Operation.user_from_id == user_id).all()
    return sum([o.amount for o in in_]) - sum([o.amount for o in out_])


async def add_operation(s: Session, operation: op_schemas.Operation) -> Operation:

    o = Operation(**operation.dict(), timestamp=datetime.datetime.now())
    s.add(o)
    s.commit()
    return o


async def get_history(
        s: Session,
        user_id: int,
        amount_gt: float = 0,
        amount_lt: float = inf,
        date_from: datetime.date = None,
        date_to: datetime.date = None
) -> t.List[Operation]:
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

    return s.query(Operation).filter(*filter_).all()

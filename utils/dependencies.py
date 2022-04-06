import datetime
import typing as t

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.operations.schemas import HistoryFilter, Operation
import db.crud as crud
from db.database import Database
from utils.enums import OperationNeedBalanceCheck


def aggregate_history_filter(
        user_id: int,
        amount_gt: t.Optional[float] = None,
        amount_lt: t.Optional[float] = None,
        date_from: t.Optional[datetime.date] = None,
        date_to: t.Optional[datetime.date] = None
) -> HistoryFilter:
    return HistoryFilter(
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
        amount_gt=amount_gt,
        amount_lt=amount_lt
    )


async def check_user_from_path_and_get_session(user_id: int, s: Session = Depends(Database.get_session)) -> Session:
    if user_id:
        if not await crud.get_user(s, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} does not exist."
            )
    return s


async def check_users_from_operation_and_get_session(
        body: Operation,
        s: Session = Depends(Database.get_session)
) -> Session:
    if body.user_to_id:
        if not await crud.get_user(s, body.user_to_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={body.user_to_id} does not exist."
            )
    if body.user_from_id:
        if not await crud.get_user(s, body.user_from_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={body.user_from_id} does not exist."
            )
    return s


async def check_users_balance_for_operation_and_get_session(
        body: Operation,
        s: Session = Depends(check_users_from_operation_and_get_session)
) -> Session:
    if OperationNeedBalanceCheck.get(body.type, False) \
            and await crud.get_balance(s, body.user_from_id) < body.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Amount exceeds users(id={body.user_from_id}) balance."
        )
    return s

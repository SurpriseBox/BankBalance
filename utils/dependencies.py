import datetime
import typing as t

from deprecation import deprecated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import db.crud as crud
from apps.operations.schemas import HistoryFilter, Operation
from db.database import Database
from utils.enums import OperationNeedBalanceCheck
from utils.exceptions import ObjectNotFoundException


def aggregate_history_filter(
        user_id: int,
        amount_gt: t.Optional[float] = None,
        amount_lt: t.Optional[float] = None,
        date_from: t.Optional[datetime.date] = None,
        date_to: t.Optional[datetime.date] = None
) -> HistoryFilter:
    """

    :param user_id:
    :param amount_gt:
    :param amount_lt:
    :param date_from:
    :param date_to:
    :return:
    """
    return HistoryFilter(
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
        amount_gt=amount_gt,
        amount_lt=amount_lt
    )


@deprecated(details='use check_user_from_path decorator from utils.decorators')
async def check_user_from_path_and_get_session(
        user_id: int,
        s: Session = Depends(Database.get_session)
) -> Session:
    """

    :param user_id:
    :param s:
    :return:
    """
    if user_id:
        try:
            await crud.get_user(s, user_id)
        except ObjectNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    return s


@deprecated(details='use check_user_from_operation decorator from utils.decorators')
async def check_users_from_operation_and_get_session(
        body: Operation,
        s: Session = Depends(Database.get_session)
) -> Session:
    """

    :param body:
    :param s:
    :return:
    """
    if body.user_to_id:
        try:
            await crud.get_user(s, body.user_to_id)
        except ObjectNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    if body.user_from_id:
        try:
            await crud.get_user(s, body.user_from_id)
        except ObjectNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    return s


@deprecated(details='use check_user_balance decorator from utils.decorators')
async def check_users_balance_for_operation_and_get_session(
        body: Operation,
        s: Session = Depends(check_users_from_operation_and_get_session)
) -> Session:
    """

    :param body:
    :param s:
    :return:
    """
    if OperationNeedBalanceCheck.get(body.type, False):
        try:
            balance = await crud.get_balance(s, body.user_from_id)
        except ObjectNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        if balance < body.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Amount exceeds users(id={body.user_from_id}) balance."
            )
    return s

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session

import db.crud as crud
from db.database import Database
from utils.dependencies import aggregate_history_filter, check_users_balance_for_operation_and_get_session
from utils.enums import Status
from .schemas import OneUserOperation, Transaction, OperationResponse, HistoryFilter

router = APIRouter(
    prefix='/operations',
    tags=['operations']
)


@router.post('/transaction', response_model=OperationResponse, status_code=status.HTTP_201_CREATED)
async def perform_transaction(
        body: Transaction,
        session: Session = Depends(check_users_balance_for_operation_and_get_session)
):
    """
    Transaction between two users.

    :param body:
    :param session:
    :return:
    """
    try:
        await crud.add_operation(session, body)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return OperationResponse(status=Status.success)


@router.post('/balance_change', response_model=OperationResponse, status_code=status.HTTP_201_CREATED)
async def perform_balance_change(
        body: OneUserOperation,
        session: Session = Depends(check_users_balance_for_operation_and_get_session)
):
    """
    Balance change operation for user.
    :param body:
    :param session:
    :return:
    """
    try:
        await crud.add_operation(session, body)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return OperationResponse(status=Status.success)


@router.get('/history')
async def get_history(
        filters: HistoryFilter = Depends(aggregate_history_filter),
        session: Session = Depends(Database.get_session)
):
    """

    :param filters:
    :param session:
    :return:
    """
    try:
        h = await crud.get_history(session, **filters.dict())
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return h

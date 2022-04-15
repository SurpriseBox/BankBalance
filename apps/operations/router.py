
import datetime
import typing as t

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import db.crud as crud
from db import models
from db.database import Database
from utils.decorators import check_user_balance, check_user_from_operation
from utils.dependencies import aggregate_history_filter
from utils.enums import Status
from .schemas import Operation, OperationOut, OneUserOperation, Transaction, OperationResponse, HistoryFilter
from .background_tasks import add_operation_to_query

app_router = APIRouter(
    prefix='/operations',
    tags=['operations']
)


@app_router.post(
    path='/transaction',
    response_model=OperationResponse,
    status_code=status.HTTP_201_CREATED
)
@check_user_from_operation
@check_user_balance
async def perform_transaction_operation(
        operation: Transaction,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(Database.get_session)
) -> OperationResponse:
    """
    Transaction between two users.

    :param operation:
    :param background_tasks:
    :param session:
    :return:
    """
    try:
        async with session.begin():
            db_operation: models.Operation = await crud.add(
                session=session,
                model=models.Operation,
                instance=operation,
                timestamp=datetime.datetime.utcnow()
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    background_tasks.add_task(add_operation_to_query, db_operation)
    return OperationResponse(status=Status.success, operation_status=db_operation.status)


@app_router.post(
    path='/balance_change',
    response_model=OperationResponse,
    status_code=status.HTTP_201_CREATED
)
@check_user_from_operation
@check_user_balance
async def perform_balance_change_operation(
        operation: OneUserOperation,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(Database.get_session)
) -> OperationResponse:
    """
    Balance change operation for user.

    :param operation:
    :param background_tasks:
    :param session:
    :return:
    """
    try:
        async with session.begin():
            db_operation: models.Operation = await crud.add(
                session=session,
                model=models.Operation,
                instance=operation,
                timestamp=datetime.datetime.utcnow()
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    background_tasks.add_task(add_operation_to_query, db_operation)
    return OperationResponse(status=Status.success, operation_status=db_operation.status)


@app_router.get(
    path='/history',
    response_model=t.List[OperationOut],
    status_code=status.HTTP_200_OK
)
async def get_history(
        filters: HistoryFilter = Depends(aggregate_history_filter),
        session: AsyncSession = Depends(Database.get_session)
) -> t.List[Operation]:
    """
    Operations history for user.

    :param filters:
    :param session:
    :return:
    """
    try:
        operations_list: t.List[models.Operation] = await crud.get_history(session, **filters.dict())
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return list(map(OperationOut.from_orm, operations_list))


from celery_app import app

from db import crud
from db.database import Database
from db.models import Operation
from utils.enums import OperationStatus, OperationNeedBalanceCheck
from utils.helper_funcs import async_to_sync


@app.task(name='operations.process_operation')
@async_to_sync
async def process_operation(operation_id: int) -> int:
    async with Database.get_session_manager() as session:
        async with session.begin():
            await crud.change_operation_status(session, operation_id, OperationStatus.in_progress)

        async with session.begin():
            operation: Operation = await crud.get(session, Operation, operation_id)
            if OperationNeedBalanceCheck.get(operation.type):
                balance = await crud.get_balance(session, operation.user_from_id)
                if balance < operation.amount:
                    await crud.change_operation_status(session, operation_id, OperationStatus.error)
                    return operation_id

            if operation.user_from_id:
                await crud.change_balance(session, operation.user_from_id, -1 * operation.amount)
            if operation.user_to_id:
                await crud.change_balance(session, operation.user_to_id, operation.amount)

            await crud.change_operation_status(session, operation_id, OperationStatus.success)
    return operation_id


@app.task(name='operations.begin_process_operation')
@async_to_sync
async def begin_process_operation(operation_id: int) -> int:
    async with Database.get_session_manager() as session:
        async with session.begin():
            await crud.change_operation_status(session, operation_id, OperationStatus.pending)
    return operation_id

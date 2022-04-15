
from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import crud
from db import models
from .exceptions import ObjectNotFoundException, TransactionRequiredException


# PATH operations decorators
def check_user_from_operation(method):
    @wraps(method)
    async def wrapper(
            operation,
            background_tasks,
            session: AsyncSession
    ):
        if operation.user_to_id:
            try:
                await crud.get(session, models.User, operation.user_to_id)
            except ObjectNotFoundException as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(e)
                )

        if operation.user_from_id:
            try:
                await crud.get(session, models.User, operation.user_from_id)
            except ObjectNotFoundException as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(e)
                )

        return await method(operation, background_tasks, session)
    return wrapper


def check_user_from_path(method):
    @wraps(method)
    async def wrapper(
            user_id: int,
            session: AsyncSession
    ):
        try:
            await crud.get(session, models.User, user_id)
        except ObjectNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )

        return await method(user_id, session)
    return wrapper


def check_user_balance(method):
    @wraps(method)
    async def wrapper(
            operation,
            background_tasks,
            session: AsyncSession
    ):
        if operation.user_from_id:
            if await crud.get_balance(session, operation.user_from_id) < operation.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Amount exceeds users(id={operation.user_from_id}) balance."
                )
        return await method(operation, background_tasks, session)
    return wrapper


# CRUD functions decorators
def transaction_required(crud_operation):
    @wraps(crud_operation)
    async def wrapper(session: AsyncSession, *args, **kwargs):
        if not session.get_transaction():
            raise TransactionRequiredException()
        return await crud_operation(session, *args, **kwargs)
    return wrapper


def transaction_if_needed(crud_operation):
    @wraps(crud_operation)
    async def wrapper(session: AsyncSession, *args, **kwargs):
        if not session.get_transaction():
            async with session.begin():
                return await crud_operation(session, *args, **kwargs)
        return await crud_operation(session, *args, **kwargs)
    return wrapper

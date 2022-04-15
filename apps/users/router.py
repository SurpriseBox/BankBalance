
from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import db.crud as crud
import db.models as models
from db.database import Database
from utils.decorators import check_user_from_path
from .schemas import BalanceOut, User, UserCreate

app_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@app_router.post(
    path='/',
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(Database.get_session)
) -> User:
    """

    :param user:
    :param session:
    :return:
    """
    try:
        async with session.begin():
            db_user: models.User = await crud.add(session, models.User,  user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_user


@app_router.get(
    path='/{user_id}',
    response_model=User
)
@check_user_from_path
async def get_user_by_id(
        user_id: int = Path(..., gt=0, title="User id"),
        session: AsyncSession = Depends(Database.get_session)
) -> User:
    """

    :param user_id:
    :param session:
    :return:
    """
    db_user: models.User = await crud.get(session, models.User, user_id)
    return db_user


@app_router.get(
    path='/{user_id}/balance',
    response_model=BalanceOut
)
@check_user_from_path
async def get_user_balance(
        user_id: int = Path(..., gt=0, title="User id"),
        session: AsyncSession = Depends(Database.get_session)
) -> BalanceOut:
    """

    :param user_id:
    :param session:
    :return:
    """
    balance = await crud.get_balance(session, user_id)
    return BalanceOut(balance=balance)

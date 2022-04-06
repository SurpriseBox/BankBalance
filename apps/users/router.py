
from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session

import db.crud as crud
from db.database import Database
from utils.enums import Status
from utils.dependencies import check_user_from_path_and_get_session
from .schemas import BalanceOut, User, UserCreate, UserResponse

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def user(
        user: UserCreate,
        session: Session = Depends(Database.get_session)
):
    """

    :param user:
    :param session:
    :return:
    """
    try:
        obj = await crud.add_user(session, user)
        resp = UserResponse(status=Status.success, user=obj)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return resp


@router.get('/{user_id}', response_model=User)
async def user(
        user_id: int = Path(..., gt=0, title="User id"),
        session: Session = Depends(check_user_from_path_and_get_session)
):
    """

    :param user_id:
    :param session:
    :return:
    """
    return await crud.get_user(session, user_id)


@router.get('/{user_id}/balance', response_model=BalanceOut)
async def balance(
        user_id: int = Path(..., gt=0, title="User id"),
        session: Session = Depends(check_user_from_path_and_get_session)
):
    """

    :param user_id:
    :param session:
    :return:
    """
    return BalanceOut(user_id=user_id, balance=await crud.get_balance(session, user_id))

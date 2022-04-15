from decimal import Decimal as pyDecimal

from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, relationship

from utils.enums import OperationType, OperationStatus

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(200), nullable=False, default='')
    last_name = Column(String(200), nullable=False, default='')
    patr_name = Column(String(200), nullable=False, default='')
    balance: pyDecimal = Column(DECIMAL(14, 4), nullable=False, default=0)


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key=True)
    amount: pyDecimal = Column(DECIMAL(14, 4), nullable=False)
    type = Column(Enum(OperationType))
    user_from_id = Column(ForeignKey('user.id'), nullable=True)
    user_to_id = Column(ForeignKey('user.id'), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    comment = Column(String(500), nullable=False, default='')
    status = Column(Enum(OperationStatus), nullable=False, default=OperationStatus.created)

    user_from = relationship('User', foreign_keys=[user_from_id])
    user_to = relationship('User', foreign_keys=[user_to_id])

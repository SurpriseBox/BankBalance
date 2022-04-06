
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship

from utils.enums import OperationType

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(200), nullable=False, default='')
    last_name = Column(String(200), nullable=False, default='')
    patr_name = Column(String(200), nullable=False, default='')


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(OperationType))
    user_from_id = Column(ForeignKey('user.id'), nullable=True)
    user_to_id = Column(ForeignKey('user.id'), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    comment = Column(String(500), nullable=False, default='')

    user_from = relationship('User', foreign_keys=[user_from_id])
    user_to = relationship('User', foreign_keys=[user_to_id])

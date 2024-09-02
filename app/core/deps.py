from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.settings import settings
from services.user_services import UserService
from services.transactions_services import TransactionService

#...
engine = create_engine(settings.DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def user_service(session:Session = Depends(get_session)) -> UserService:
    return UserService(session)

def get_transaction_service(session:Session = Depends(get_session)) -> TransactionService:
    return TransactionService(session)
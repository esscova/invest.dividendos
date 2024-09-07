from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session

from core.deps import get_session
from core.auth import get_current_user
from db.models import User
from db.schemas import TransactionResponse
from services import portfolio
#...

router = APIRouter(prefix='/user/transactions', tags=['transactions'])
db_session = Annotated[Session, Depends(get_session)]
current_user = Annotated[User,Depends(get_current_user)]


@router.get('/', response_model=TransactionResponse)
async def read_transactions(db:db_session, user:current_user):
    return portfolio.PortfolioService(db,user).get_all_transactions()

@router.get('/date/{date}', response_model=TransactionResponse)
async def get_transactions_by_date(date:str, db:db_session, user:current_user):
    service = portfolio.PortfolioService(db=db,user=user)
    return service.get_transactions_by_date(date=date)

@router.get('/ticker/{ticker}', response_model=TransactionResponse)
async def get_transactions_by_ticker(ticker:str, db:db_session, user:current_user):
    service = portfolio.PortfolioService(db,user)
    return service.get_transactions_by_ticker(ticker)

@router.get('/type/{type}', response_model=TransactionResponse)
async def get_transactions_type(type:str,db:db_session,user:current_user):
    service = portfolio.PortfolioService(db,user)
    return service.get_transactions_by_type(type)

@router.get('/date/period/{start_date}/{end_date}', response_model=TransactionResponse)
async def get_transactions_by_period(start_date:str, end_date:str, db:db_session, user:current_user):
    service = portfolio.PortfolioService(db,user)
    return service.get_transactions_by_date_range(start_date, end_date)
from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from core.deps import get_session
from core.auth import get_current_user
from db.models import Transaction, User
from db.schemas import PortfolioSchema

#...

router = APIRouter(prefix='/portfolio', tags=['portfolio'])



@router.get('/', response_model=List[PortfolioSchema])
async def get_portfolio(session:Session = Depends(get_session),user:User=Depends(get_current_user)):
    
    query = (
        select(Transaction.ticker, func.sum(Transaction.quantidade).label('quantidade'))
        .where(Transaction.user_id==user.id)
        .group_by(Transaction.ticker)
    )
    result = session.execute(query)
    portfolio = [
        PortfolioSchema(ticker=k.ticker, quantidade=k.quantidade) for k in result
    ]
    return portfolio
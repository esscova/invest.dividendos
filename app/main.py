from fastapi import FastAPI


from routes.auth_routes import router as auth_router
from routes.dividends_routes import router as dividends_router
from routes.user_routes import router as user_router
from routes.transaction_routes import router as transaction_router

#...

app = FastAPI(title='Invest.dividendos',version="0.0.1", openapi_url='/invest.dividendos')

#...


@app.get('/')
def home():
    return{'ping':'pong'}

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, distinct, func
from core.deps import get_session, get_transaction_service
from core.auth import get_current_user
from services.transactions_services import TransactionService
from db.models import Transaction, User

class Portfolio(BaseModel):
    ticker:str
    quantidade:int

@app.get('/portfolio', response_model=List[Portfolio])
async def get_portfolio(session:Session = Depends(get_session), transaction:TransactionService=Depends(get_transaction_service), user:User=Depends(get_current_user)):
    
    query = select(Transaction.ticker, func.sum(Transaction.quantidade).label('quantidade')).where(Transaction.user_id==user.id).group_by(Transaction.ticker)
    result = session.execute(query)
    portfolio = [
        Portfolio(ticker=k.ticker, quantidade=k.quantidade) for k in result
    ]
    return portfolio

app.include_router(auth_router)
app.include_router(dividends_router)
app.include_router(user_router)
app.include_router(transaction_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8000, log_level="info", reload=True)

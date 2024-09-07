from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import Transaction, User
from db.schemas import TransactionResponse

from typing import List, Optional
#...

class PortfolioService:
    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user
    
    def _get_transactions(self, filters:Optional[List] = None) -> TransactionResponse:
        query = select(Transaction).where(Transaction.user_id == self.user.id)
        
        if filters:
            query = query.where(*filters)
        
        transactions = self.db.scalars(query).all()
        return TransactionResponse(data=transactions)

    def get_all_transactions(self) -> TransactionResponse:
        return self._get_transactions()

    def get_transactions_by_date(self, date: str) -> TransactionResponse:
        return self._get_transactions([Transaction.data == date])

    def get_transactions_by_ticker(self, ticker: str) -> TransactionResponse:
        return self._get_transactions([Transaction.ticker==ticker])
    
    def get_transactions_by_type(self, type:str) -> TransactionResponse:
        return self._get_transactions([Transaction.tipo==type])
    
    def get_transactions_by_date_range(self, start_date:str, end_date:str) -> TransactionResponse:
        return self._get_transactions([Transaction.data >= start_date, Transaction.data <= end_date])
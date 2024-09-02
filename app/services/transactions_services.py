from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Transaction
from db.schemas import BaseTransaction, ResponseTransaction

#...

class TransactionService:
    def __init__(self, session:Session) -> Session:
        self.session = session

    def create_transaction(
            self,
            transaction:BaseTransaction,
            user_id:int
        ) -> Transaction:
        
        db_transaction = Transaction(
            user_id=user_id,
            ativo=transaction.ativo,
            quantidade=transaction.quantidade,
            preco=transaction.preco,
            transaction=transaction.transaction,
        )

        self.session.add(db_transaction)
        self.session.commit()
        self.session.refresh(db_transaction)

        return db_transaction
    
    def get_transactions(
            self,
            user_id:int
    ) -> List[Transaction]:
        
        return self.session.scalars(
            select(Transaction).where(Transaction.user_id == user_id)
        ).all()
    
    def get_transaction_by_id(
            self,
            transaction_id:int,
            user_id:int
    ) -> Transaction:
        
        return self.session.scalar(
            select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user_id)
        )

    def get_transaction_by_ticker(
            self,
            ticker:str,
            user_id:int
    ) -> List[Transaction]:
        
        return self.session.scalars(
            select(Transaction).where(Transaction.ativo == ticker, Transaction.user_id == user_id)
        ).all()
    
    def update_transaction(
            self,
            transaction_id:int,
            transaction:BaseTransaction,
            user_id:int,
    ) -> Transaction:
        
        transaction_db = self.get_transaction_by_id(transaction_id,user_id)        

        if transaction_db:
            transaction_db.ativo = transaction.ativo
            transaction_db.transaction = transaction.transaction
            transaction_db.quantidade = transaction.quantidade
            transaction_db.preco = transaction.preco

            self.session.commit()
            self.session.refresh(transaction_db)
        
        return transaction_db
    
    def delete_transaction(
            self,
            transaction_id:int,
            user_id:int
    ) -> None:
        
        transaction_db = self.get_transaction_by_id(transaction_id, user_id)

        if transaction_db:
            self.session.delete(transaction_db)
            self.session.commit()
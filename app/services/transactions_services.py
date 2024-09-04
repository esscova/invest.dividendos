from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.models import Transaction
from db.schemas import BaseTransaction

#...

class TransactionService:
    def __init__(self, session:Session) -> Session:
        self.session = session

    def create_transaction(
            self,
            transaction:BaseTransaction,
            user_id:int
        ) -> Transaction:
        try:
            db_transaction = Transaction(
                user_id=user_id,
                ticker=transaction.ticker,
                quantidade=transaction.quantidade,
                preco_unitario=transaction.preco_unitario,
                tipo=transaction.tipo,
                data=transaction.data
            )

            self.session.add(db_transaction)
            self.session.commit()
            self.session.refresh(db_transaction)

            return db_transaction
        
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Erro ao criar transação: {str(e)}')
        
    def get_transactions(
            self,
            user_id:int
    ) -> List[Transaction]:
        try:
            return self.session.scalars(
                select(Transaction).where(Transaction.user_id == user_id)
            ).all()
        except Exception as e:
            raise ValueError(f'Erro ao buscar transações:{str(e)}')
        
    def get_transaction_by_id(
            self,
            transaction_id:int,
            user_id:int
    ) -> Transaction:
        try:
            return self.session.scalar(
                select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user_id)
            )
        except Exception as e:
            raise ValueError (f'Erro ao buscar transação: {str(e)}')
        
    def get_transaction_by_ticker(
            self,
            ticker:str,
            user_id:int
    ) -> List[Transaction]:
        
        try:
            return self.session.scalars(
                select(Transaction).where(Transaction.ativo == ticker, Transaction.user_id == user_id)
            ).all()
        except Exception as e:
            raise ValueError(f'Erro ao buscar transação: {str(e)}')
    
    def update_transaction(
            self,
            transaction_id:int,
            transaction:BaseTransaction,
            user_id:int,
    ) -> Transaction:
        
        try:
            transaction_db = self.get_transaction_by_id(transaction_id,user_id)        

            if transaction_db:
                transaction_db.ticker = transaction.ticker
                transaction_db.tipo = transaction.tipo
                transaction_db.quantidade = transaction.quantidade
                transaction_db.preco_unitario = transaction.preco_unitario
                transaction_db.data = transaction.data

                self.session.commit()
                self.session.refresh(transaction_db)
            
            return transaction_db
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Erro ao editar a transação: {str(e)} ')
        
    def delete_transaction(
            self,
            transaction_id:int,
            user_id:int
    ) -> None:
        try:
            transaction_db = self.get_transaction_by_id(transaction_id, user_id)

            if transaction_db:
                self.session.delete(transaction_db)
                self.session.commit()
            else:
                raise ValueError(f'Transação não encontrada: ID {transaction_id}')
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f'Erro ao excluir a transação: {str(e)}')
       
        except Exception as e:
            raise ValueError(f'Erro ao excluir transação: {str(e)}')
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.deps import get_session
from core.auth import get_current_user
from db.schemas import BaseTransaction, ResponseTransaction
from db.models import User, Transaction

#...

router = APIRouter(
    prefix='/transactions',
    tags=['transactions']
    )

#...

@router.post('/',
             response_model=BaseTransaction,
             status_code=HTTPStatus.CREATED,
             summary='Registro de transações',
             description='Esta rota registra as movimentações de compra e venda de ativos.'
             )
def up_transaction(
    transaction:BaseTransaction,
    session:Session = Depends(get_session),
    user:User = Depends(get_current_user),
    ):
    
    db_transaction = Transaction(
        user_id=user.id,
        ativo=transaction.ativo,
        quantidade=transaction.quantidade,
        preco=transaction.preco,
        transaction=transaction.transaction,
    )

    try:
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)
        return db_transaction
    
    except:
        print('nao foi')
        session.rollback()

@router.get('/',
            status_code=HTTPStatus.CREATED,
            response_model=List[ResponseTransaction],
            summary='Lista de transações',
            description='Esta rota retorna uma lista de transações de um usuário logado.'
            )
def get_transactions(
    session:Session = Depends(get_session),
):
    transactions_db = session.scalars(select(Transaction)).all()

    return transactions_db
from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.deps import get_session
from core.auth import get_current_user
from db.schemas import BaseTransaction
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
        session.rollback()
        print('nao foi')
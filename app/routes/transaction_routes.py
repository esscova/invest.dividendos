from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.deps import get_session
from core.auth import get_current_user
from db.schemas import BaseTransaction, ResponseTransaction
from db.models import User, Transaction

# ...

router = APIRouter(prefix="/transactions", tags=["transactions"])

# ...


@router.post(
    "/",
    response_model=BaseTransaction,
    status_code=HTTPStatus.CREATED,
    summary="Registro de transações",
    description="Esta rota registra as movimentações de compra e venda de ativos.",
)
def create_transaction(
    transaction: BaseTransaction,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
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
        print("nao foi")
        session.rollback()


@router.get(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=List[ResponseTransaction],
    summary="Lista de transações",
    description="Esta rota retorna uma lista de transações de um usuário logado.",
)
def get_transactions(
    session: Session = Depends(get_session), user: User = Depends(get_current_user)
):
    transactions_db = session.scalars(select(Transaction)).all()

    return transactions_db


@router.get("/{ticker}", status_code=HTTPStatus.OK, response_model=List[ResponseTransaction])
def get_transaction(
    ticker: str,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):

    try:
        transactions = session.scalars(
            select(Transaction).where(
                Transaction.ativo == ticker, Transaction.user_id == user.id
            )
        ).all()

        if not transactions:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Não foram encontradas transações para o ticker: {ticker}",
            )
        return transactions

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao tentar buscar informações: {str(e)}",
        )

@router.put('/{transaction_id}', response_model=ResponseTransaction)
def update_transaction(
    transaction_id:int,
    transaction:Transaction,
    user:User = Depends(get_current_user),
    session:Session = Depends(get_session),
    ):
        transaction_db = session.scalar(
            select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user.id)
        )

        if transaction_db:
            transaction_db.ativo = transaction.ativo
            transaction_db.transaction = transaction.transaction
            transaction_db.quantidade = transaction.quantidade
            transaction_db.preco = transaction.preco

        session.commit()
        session.refresh(transaction_db)

        return transaction_db

@router.delete('/{transaction_id}')
def delete_transaction(
    transaction_id:int,
    user:User = Depends(get_current_user),
    session:Session = Depends(get_session)
):
    transaction_db = session.scalar(
        select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user.id)
    )

    if transaction_db:
        session.delete(transaction_db)
        session.commit()
    
    return {'message':'Registro deletado com sucesso'}
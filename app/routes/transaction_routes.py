from http import HTTPStatus
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.deps import get_session, get_transaction_service
from core.auth import get_current_user
from db.schemas import BaseTransaction, ResponseTransaction
from db.models import User, Transaction
from services.transactions_services import TransactionService
# ...

router = APIRouter(prefix="/transactions", tags=["transactions"])

CurrentUser = Annotated[User, Depends(get_current_user)]
ServiceTransaction = Annotated[TransactionService, Depends(get_transaction_service)]

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
    user: CurrentUser,
    service: ServiceTransaction,
):
    try:
        db_transaction = service.create_transaction(transaction, user.id)
        return db_transaction

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=List[ResponseTransaction],
    summary="Lista de transações",
    description="Esta rota retorna uma lista de transações de um usuário logado.",
)
def get_transactions(
    user:CurrentUser,
    service:ServiceTransaction
    ):
    try:
        return service.get_transactions(user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/{ticker}", 
    status_code=HTTPStatus.OK, 
    response_model=List[ResponseTransaction]
)
def get_transaction(
    ticker: str,
    user: CurrentUser,
    service:ServiceTransaction,
):

    try:
        transactions = service.get_transaction_by_ticker(ticker, user.id)

        if not transactions:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Não foram encontradas transações para o ticker: {ticker}",
            )
        return transactions

    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/{transaction_id}", response_model=ResponseTransaction)
def update_transaction(
    transaction_id: int,
    transaction: Transaction,
    user: CurrentUser,
    service:ServiceTransaction
):
    try:
        transaction_db = service.update_transaction(transaction_id, transaction, user.id)

        if not transaction_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Registro não encontrado'
            )

        return transaction_db
    
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    user: CurrentUser,
    service:ServiceTransaction,
):
    try:
        service.delete_transaction(transaction_id,user.id)
        return {'message':'Registro deletado com sucesso'}
    
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

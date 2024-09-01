from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Annotated

from db.schemas import DividendsSchema, ResponseDividend
from services.transactions_services import DividendService

#...
router = APIRouter(prefix='/agenda', tags=['dividends'])
services = Annotated[DividendService, Depends(DividendService)]
#...

@router.get(
    '/acoes',
    status_code=HTTPStatus.OK, 
    response_model=List[DividendsSchema],
    summary='Dividendos de ações',
    description='Esta rota retorna a agenda de dividendos de ações'
    )
async def get_acoes(
    ano:int,
    mes:int,
    dividend_service:services
    ):
    
    try:
        return await dividend_service.get_dividends(ano,mes,tipo=1)
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    '/acoes/{ticker}',
    status_code=HTTPStatus.OK, 
    response_model=List[ResponseDividend],
    summary='Dividendos de uma ação específica',
    description='Esta rota retorna os dados do dividendo de uma ação específica.'
)
async def get_dividend_by_ticker(
    ticker: str,
    dividend_service:services,
    ano: int,
    mes: int, 
    ):
    
    return await dividend_service.get_dividends_by_ticker(tipo=1, ticker=ticker, ano=ano, mes=mes)
    
@router.get(
    '/fiis',
    status_code=HTTPStatus.OK, 
    response_model=List[DividendsSchema],
    summary='Dividendos de FIIs',
    description='Esta rota retorna a agenda de dividendos de fundos imobiliários'
    )
async def get_fiis(
    ano:int,
    mes:int,
    dividend_service:services
    ):
    
    try:
        return await dividend_service.get_dividends(ano,mes,tipo=2)
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    '/fiis/{ticker}',
    status_code=HTTPStatus.OK, 
    response_model=List[ResponseDividend],
    summary='Dividendos de um fii específico',
    description='Esta rota retorna os dados de proventos de um fundo imobiliário específico.'
)
async def get_dividend_by_ticker(
    ticker: str,
    dividend_service:services,
    ano: int,
    mes: int, 
    ):
    
    return await dividend_service.get_dividends_by_ticker(tipo=2, ticker=ticker, ano=ano, mes=mes)
# ...
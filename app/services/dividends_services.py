from http import HTTPStatus
from typing import List, Dict, Optional
from fastapi import HTTPException

from scrap.coletor import coletar_dados
from core.settings import settings

#...

class DividendService:
    def __init__(self):
        self.header = settings.HEADER

    async def _fetch(self, ano:int, mes:int, tipo:int) -> Optional[List[Dict[str,str]]]:
        """metodo privado para coletar dados de dividendos"""
        try:
            data = await coletar_dados(self.header, ano, mes, tipo)
            
            if not data:
                return None
            
            return data
        
        except Exception as e:
            print(f'Erro em coletar dados: {e}')
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro coletando dados de dividendos'
            )
 
    async def get_dividends(self, ano:int, mes:int, tipo:int) -> List[Dict[str,str]]:
        """Este método coleta e retorna dividendos para um ano e mês específico"""
        
        data = await self._fetch(ano, mes, tipo)

        if data is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Não foram encontrados dados para {mes}/{ano}'
            )
        
        return data

    async def get_dividends_by_ticker(self, tipo: int, ticker: str, ano: int, mes: int ) -> List[Dict[str, str]]:
        """Este método coleta e retorna dividendos para um ano e mês de um ativo específico pelo ticker"""
        
        data = await self._fetch(ano, mes, tipo)

        if data is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Não foram encontrados dados para {mes}/{ano}'
            )
        
        result = [x for x in data if x['Ticker'].upper() == ticker.upper()]

        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'No dividends found for ticker: {ticker}'
            )
        
        return result
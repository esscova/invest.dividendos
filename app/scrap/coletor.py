import requests
import aiohttp
from datetime import datetime
from bs4 import BeautifulSoup as bs
from typing import List, Dict, Optional

from core.settings import settings

#...

def criar_sessao(header: dict) -> requests.Session:
    """Cria uma sessão HTTP para reutilizar conexões"""
    session = requests.Session()
    session.headers.update(header)
    return session

def coletar_pagina(sessao: requests.Session, url: str) -> Optional[bs]:
    """Realiza a requisição da página e retorna um objeto BeautifulSoup"""
    try:
        response = sessao.get(url)
        response.raise_for_status()
        return bs(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f'Erro ao coletar a página: {e}')
        return None

def expandir_ano(data: str) -> str:
    """Expande o ano de dois dígitos para quatro dígitos"""
    dia, mes, ano = data.split('/')
    if len(ano) == 2:
        ano = '20' + ano
    return f'{dia}/{mes}/{ano}'

def extrair_dados_da_linha(row: bs) -> Optional[Dict[str, str]]:
    """Extração de dados de uma linha da tabela com conversão de datas"""
    columns = row.find_all('td')
    
    if not columns:
        return None

    ativo_tag = columns[0].find('a')
    nome_tag = columns[0].find('span', class_='text-muted')
    
    if ativo_tag and nome_tag:
        ativo = ativo_tag.get_text(strip=True)
        nome = nome_tag.get_text(strip=True)
        data_com = columns[1].get_text(strip=True)
        data_pgto = columns[2].get_text(strip=True)
        tipo = columns[3].get_text(strip=True)
        valor_str = columns[4].get_text(strip=True).replace('.', '').replace(',', '.')
        
        try:
            valor = float(valor_str)
        except ValueError:
            print(f"Erro ao converter valor: {valor_str}")  
            valor = 0.0  
        
        
        try:
            data_com = datetime.strptime(expandir_ano(data_com), '%d/%m/%Y').date()
            data_pgto = datetime.strptime(expandir_ano(data_pgto), '%d/%m/%Y').date()
        except ValueError as e:
            print(f"Erro ao converter data: {e}")
            return None
        
        return {
            'Ticker': ativo,
            'Instituição': nome,
            'Data_com': data_com,
            'Data_Pgto': data_pgto,
            'Tipo': tipo,
            'Valor': valor
        }
    return None

async def coletar_dados(header: dict, ano: int, mes: int, tipo: int = 1) -> List[Dict[str, str]]:
    """Coleta e processa os dados de dividendos para o ano, mês e tipo fornecidos"""

    url = settings.URL.format(tipo=tipo, ano=ano, mes=mes)
       
    async with aiohttp.ClientSession(headers=header) as sessao:
        async with sessao.get(url) as resposta:
            if resposta.status != 200:
                return []
            
            site = await resposta.text()
            site = bs(site, 'html.parser')
            
            dados = []
            rows = site.find_all('tr')
            
            for row in rows:
                dado = extrair_dados_da_linha(row)
                if dado:
                    dados.append(dado)
    
    return dados

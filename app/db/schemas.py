from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from enum import Enum

class UserSchema(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserPublic(BaseModel):
    id:int
    username:str
    email:EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    users: list[UserPublic]

class Message(BaseModel):
    message:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str | None = None

class UserInfos(UserPublic):
    created_at:datetime
    updated_at:datetime

class DividendsSchema(BaseModel):
    Ticker: str
    Instituição: str
    Data_com: date
    Data_Pgto: date
    Tipo: str
    Valor: float

    model_config = ConfigDict(from_attributes=True)

class ResponseDividend(BaseModel):
    Instituição: str
    Data_com: date
    Data_Pgto: date
    Tipo: str
    Valor: float

from db.models import TransactionType

class BaseTransaction(BaseModel):
    data:date    
    tipo:TransactionType
    ticker:str 
    quantidade:int 
    preco_unitario:float
    
    model_config = ConfigDict(from_attributes=True)

class ResponseTransaction(BaseTransaction):
    id:int
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)

###

class PortfolioSchema(BaseModel):
    ticker:str
    quantidade:int

from typing import List
class Transaction(BaseModel):
    data:date    
    tipo:TransactionType
    ticker:str 
    quantidade:int 
    preco_unitario:float
    model_config = ConfigDict(from_attributes=True)
    
class TransactionResponse(BaseModel):
    data:List[Transaction]
from datetime import datetime, timedelta
from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from core.settings import settings

class Security:
    def __init__(self):
        self.pwd_context = PasswordHash.recommended()
    
    def create_access_token(self,data:dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({'exp':expire})
        encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt
    
    def get_password_hash(self,password:str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password:str, hashed_password:str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
security:Security = Security()
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.orm import Session

from jwt import DecodeError, decode

from core.deps import get_session
from db.models import User
from db.schemas import TokenData

from core.settings import settings

#...

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth')

def get_current_user(
    session:Session = Depends(get_session),
    token:str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='could not validate credentials',
        headers={'WWW-Authenticate':'Bearer'}
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username:str = payload.get('sub')

        if not username:
            raise credentials_exception
        
        token_data = TokenData(username=username)

    except DecodeError:
        raise credentials_exception
    
    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if not user:
        raise credentials_exception
    
    return user
from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.deps import user_service
from db.schemas import Token
from services.user_services import UserService

#...

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
UserServices = Annotated[UserService, Depends(user_service)]

#...

@router.post('/', 
             status_code=HTTPStatus.CREATED, 
             response_model=Token,
             summary='Login for access Token',
             description='Use your email as "username" and your password to obtain an access token.'
             )
def login_for_access_token(
    form_data:OAuth2Form, 
    user_service:UserServices):
    
    return user_service.access_token(form_data)
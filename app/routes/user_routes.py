from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from core.auth import get_current_user
from core.deps import user_service
from db.schemas import Message, UserPublic, UserSchema, UserInfos
from db.models import User
from services.user_services import UserService

#...
router = APIRouter(prefix='/users',tags=['users'])

CurrentUser = Annotated[User, Depends(get_current_user)]
services = Annotated[UserService, Depends(user_service)]
#...

@router.post('/',
            status_code=HTTPStatus.CREATED,
            response_model=UserPublic,
            summary='Cadastrar novo usuario',
            description='Rota para criar novos usuarios, escolha seu username, email e uma senha.'
            )
def create_user(
    user:UserSchema, 
    service:services
):
    try:
        return service.create_user(user)
        
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    
    except IntegrityError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Erro de integridade ao criar usuário, verifique os dados fornecidos.'
        )

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro interno ao criar usuário, tente novamente mais tarde.'
        )

@router.get('/me',
            status_code=HTTPStatus.OK,
            response_model=UserInfos,
            summary='Informações do perfil',
            description='Uma vez autenticado, esta rota retornará dados registrados no perfil.'
            )
def get_me(current_user:CurrentUser):
    
    return current_user

@router.put('/',
            response_model=UserPublic, 
            summary='Atualizar dados', 
            description='Esta rota permite que um usuário autenticado possa editar seus dados.'
            )
def update_user(
    user:UserSchema,
    current_user:CurrentUser,
    service:services
):
    updated_user = service.update_user(current_user.id,user)

    if not updated_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
        )
    return updated_user

@router.delete('/delete', 
               response_model=Message,
               summary='Excluir registro',
               description='Por esta rota um usuário autenticado pode excluir sua conta.'
               )
def delete_account(current_user:CurrentUser, service:services):

    deleted_user = service.delete_user(current_user.id)

    if not deleted_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted"}

##########

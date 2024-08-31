from http import HTTPStatus

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.models import User
from db.schemas import UserSchema, Token
from core.security import security

#...

class UserService:
    def __init__(self, session:Session):
        self.session = session
    
    def get_current_user(self):
        from core.auth import get_current_user
        current_user:User = Depends(get_current_user)

        return current_user

    def create_user(self, user:UserSchema):
        try:
            db_user = User(
                username=user.username,
                password=security.get_password_hash(user.password),
                email=user.email
            )

            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)

            return db_user
        
        except IntegrityError as e:
            
            self.session.rollback()
            
            if 'UNIQUE constraint failed: users.username' in str(e):                
                raise ValueError("Usuário com este nome de usuário já existe.")
           
            elif 'UNIQUE constraint failed: users.email' in str(e):
                raise ValueError("Usuário com este email já existe.")
           
            else:
                raise e

    def get_user_by_id(self, user_id:int):
        result = self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    def get_user_by_email(self, email:str):
        result = self.session.execute(
            select(User).where(User.email == email)
        )
        return  result.scalar_one_or_none()

    def authenticate_user(self, email:str, password:str):
        user = self.get_user_by_email(email)
        
        if not user:
            print(f'{email} not found')
            return False
        
        if not security.verify_password(password, user.password):
            print(f'password for {email} is incorrect')
            return False
        
        return user
    
    def access_token(self, form_data:OAuth2PasswordRequestForm) -> Token:
        user = self.authenticate_user(form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Incorrect email or password'
            )
        
        access_token = security.create_access_token(data={'sub':user.email})
        return Token(access_token=access_token, token_type='bearer')        

    def get_users(self, skip:int, limit:int):
        users = self.session.scalars(select(User).offset(skip).limit(limit)).all() 
        return {'users': users}

    def update_user(self, user_id:int, user:UserSchema):
        db_user = self.get_user_by_id(user_id)
        
        if db_user:
            db_user.username = user.username
            db_user.password = security.get_password_hash(user.password)
            db_user.email = user.email

            self.session.commit()
            self.session.refresh(db_user)

            return db_user
        
        return None
    
    def delete_user(self, user_id:int):
        db_user = self.get_user_by_id(user_id)
        
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
        
        return db_user 
    


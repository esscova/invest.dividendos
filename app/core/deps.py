from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from core.settings import settings
from fastapi import Depends
from services.user_services import UserService

engine = create_engine(settings.DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def user_service(session:Session = Depends(get_session)) -> UserService:
    return UserService(session)
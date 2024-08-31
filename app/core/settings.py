from typing import Dict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    URL:str = 'https://agendadividendos.com/app/ajax/agenda.php?a=get-mes&tipo={tipo}&ano={ano}&mes={mes}tipoData=1'

    HEADER: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    DATABASE_URL: str

    SECRET_KEY:str

    ALGORITHM:str

    ACCESS_TOKEN_EXPIRE_MINUTES:int


settings: Settings = Settings()
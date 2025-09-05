from pydantic_settings import BaseSettings
from pydantic import EmailStr
from typing import Optional

class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    internal_api_key: Optional[str] = "devkey"

    email_enable: bool = False
    email_host: str = "smtp.gmail.com"
    email_port: int = 465
    email_username: Optional[str] = None
    email_password: Optional[str] = None
    email_secure: bool = True
    email_from: Optional[EmailStr] = None

    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

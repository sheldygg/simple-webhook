from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    url_domain: str
    url_path: str
    server_host: str
    server_port: int
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()
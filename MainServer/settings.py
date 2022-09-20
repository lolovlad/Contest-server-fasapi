from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    database_name: str = "DataBaseFile/Context.db"
    files: str = "Files"


settings = Settings(_env_file="settings_server.env", _env_file_encoding="utf-8")

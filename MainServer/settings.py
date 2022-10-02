from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "192.168.174.6"
    server_port: int = 8000
    database_name: str = "DataBaseFile/Context.db"
    static_path: str = "Files"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600 * 12


settings = Settings(_env_file="settings_server.env", _env_file_encoding="utf-8")

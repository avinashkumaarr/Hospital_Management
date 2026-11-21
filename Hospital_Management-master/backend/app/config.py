import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    PROJECT_NAME: str = "MediLink — Unified Hospital Management System"
    VERSION: str = "4.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "medilink-super-secret-key-change-in-production-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database Settings: default to sqlite for local zero-config dev, mysql when configured
    DB_ENGINE: str = os.getenv("DB_ENGINE", "sqlite")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "medilink_db")
    
    SQLITE_PATH: str = str(BASE_DIR / "medilink.db")
    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    
    @property
    def mysql_url(self) -> str:
        pwd = f":{self.MYSQL_PASSWORD}" if self.MYSQL_PASSWORD else ""
        return f"mysql+mysqlconnector://{self.MYSQL_USER}{pwd}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
    
    @property
    def sqlite_url(self) -> str:
        clean_path = self.SQLITE_PATH.replace("\\", "/")
        return f"sqlite:///{clean_path}"

settings = Settings()

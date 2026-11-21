import os
import logging
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.config import settings

logger = logging.getLogger("medilink.db")

Base = declarative_base()

def get_engine():
    if settings.DB_ENGINE.lower() == "mysql":
        logger.info(f"Connecting to MySQL database: {settings.mysql_url}")
        engine = create_engine(
            settings.mysql_url,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        return engine, "mysql"

    # Default: Local SQLite database
    logger.info(f"Connecting to SQLite database: {settings.sqlite_url}")
    engine = create_engine(
        settings.sqlite_url,
        connect_args={"check_same_thread": False}
    )
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    return engine, "sqlite"

engine, active_db_engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

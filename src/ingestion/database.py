from sqlalchemy import create_engine
from src.config import DATABASE_URL


def get_engine():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not configured.")

    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )
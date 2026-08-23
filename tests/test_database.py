from sqlalchemy import text

from src.ingestion.database import get_engine


def test_database_connection():
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
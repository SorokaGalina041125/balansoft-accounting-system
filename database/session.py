"""PostgreSQL connection (optional)."""

import os
from typing import Optional

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from dotenv import load_dotenv

    load_dotenv()
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/balansoft_db",
    )

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db() -> Optional[object]:
        """Get database session."""
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()

except ImportError:
    engine = None
    SessionLocal = None
    get_db = None

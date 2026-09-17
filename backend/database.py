"""
Shared database configuration for Celestial Portal
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

# Database URL from environment or default for local development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/crystal_vision"
)

# Create engine with connection pooling and pre-ping to validate connections
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Configure SQLAlchemy to use UTC timezone
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Configure PostgreSQL connection for UTC timezone"""
    dbapi_conn.execute("SET timezone='UTC'")

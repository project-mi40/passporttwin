#######################################################
#Este archivo para gestionar el pool de conexiones hacia 
# PostgreSQL mediante SQLAlchemy
#######################################################

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://passporttwin:devpassword@postgres:5432/passporttwin"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
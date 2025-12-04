from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import load_config

engine = create_engine(load_config().DATABASE_URL, pool_pre_ping=True, pool_size=20, max_overflow=0,pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

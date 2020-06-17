from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.storage import settings

# Витрина данных
engine_mart = create_engine(settings.DB_DATA_MART)
MartBase = declarative_base(bind=engine_mart)

session_mart = sessionmaker()
session_mart.configure(bind=engine_mart)

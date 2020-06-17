from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.storage import settings

# Информационная база данных АСКУЭ РС
engine_is = create_engine(settings.DB_IS_ASKUE)
IS_AskueBase = declarative_base(bind=engine_is)

session_is = sessionmaker()
session_is.configure(bind=engine_is)

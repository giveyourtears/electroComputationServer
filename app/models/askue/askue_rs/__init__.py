from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from app.storage import settings

# АСКУЭ распределительной сети
engine_rs_main = create_engine(settings.DB_ASKUE_RS['main_db'])
engine_rs_data = create_engine(settings.DB_ASKUE_RS['data_db'])
RsMainBase = declarative_base(bind=engine_rs_main)
RsDataBase = declarative_base(bind=engine_rs_data)

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
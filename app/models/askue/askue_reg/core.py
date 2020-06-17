from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from app.storage import settings

# АСКУЭ региональных энергообъектов
engine_reg_main = create_engine(settings.DB_ASKUE_REGION['main_db'])
engine_reg_data = create_engine(settings.DB_ASKUE_REGION['data_db'])
RegMainBase = declarative_base(bind=engine_reg_main)
RegDataBase = declarative_base(bind=engine_reg_data)

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATETIME_FORMAT_F = "%Y-%m-%d %H:%M:%S.%f"

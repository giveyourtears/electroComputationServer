from typing import Dict, List
import os
import yaml
import pytz


settings_file_name = 'settings.yaml'
if os.environ.get('DEV_PG_HOST') is not None:
    settings_file_name = 'settings.dev.yaml'


DB_ASKUE_REGION: Dict[str, str]
DB_ASKUE_RS: Dict[str, str]
SCHEDULE_BALANS: List[str]
LOGGING: Dict[str, str]
DB_DATA_MART: str
DB_IS_ASKUE: str


file_name = os.path.abspath(os.path.dirname(__file__))
file_name = os.path.join(file_name, settings_file_name)
with open(file_name, 'r') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

DB_ASKUE_REGION = cfg['DB_ASKUE_REGION']
DB_ASKUE_RS = cfg['DB_ASKUE_RS']
SCHEDULE_BALANS = cfg['SCHEDULE_BALANS']
DB_DATA_MART = cfg['DB_DATA_MART']
DB_IS_ASKUE = cfg['DB_IS_ASKUE']
LOGGING = cfg['LOGGING']
TIME_ZONE = pytz.timezone(cfg['TIME_ZONE'])
BALANCE_RECALC_DEEP = cfg['BALANCE_RECALC_DEEP']


def __init_DB_DATA_MART():
    address = os.environ.get('DEV_PG_HOST')
    if address is not None:
        global DB_DATA_MART
        DB_DATA_MART = DB_DATA_MART.replace('${DEV_PG_HOST}', address)

def __init_DB_IS_ASKUE():
    address = os.environ.get('DEV_PG_HOST')
    if address is not None:
        global DB_IS_ASKUE
        DB_IS_ASKUE = DB_IS_ASKUE.replace('${DEV_PG_HOST}', address)


__init_DB_DATA_MART()
__init_DB_IS_ASKUE()

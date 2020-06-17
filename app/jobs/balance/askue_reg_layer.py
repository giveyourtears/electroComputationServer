from logging import Logger
from app.models.askue import DataDouble, AccountPoint
from typing import List, Union
from pypika import Query, MSSQLQuery, Table, Order, Parameter  # type: ignore
from pypika.functions import DistinctOptionFunction
from pendulum import datetime as penddt
import pytz
from datetime import datetime
from app.storage import settings

from app.models.askue.askue_reg import engine_reg_data, engine_reg_main
from app.jobs.balance.askue_layer_base import AskueLayerBase

class ToTicks(DistinctOptionFunction):
    """
        Класс определения функции ToTicks
        """

    def __init__(self, schema: str, term, alias=None):
        super(ToTicks, self).__init__(f'{schema}."ToTicks"', term, alias=alias)


class ToDateTime2(DistinctOptionFunction):
    """
    Класс определения функции ToDateTime2
    """

    def __init__(self, schema: str, term, alias=None):
        super(ToDateTime2, self).__init__(f'{schema}."ToDateTime2"', term, alias=alias)

class DalReg(AskueLayerBase):
    """
    Класс DAL работы с БД АСКУЭ региональных энергообъектов
    """
    def __init__(self, logger: Logger):
        super().__init__(logger, engine_reg_main, engine_reg_data, MSSQLQuery)

    def read_tag_values(self, tag_id: int, start_local: datetime, end_local: datetime) -> List[DataDouble]:
        """
        Выполняет чтение значений тега за указанный период времени
        :param tag_id: идентификатор тега
        :param start_local: начальное время чтения (локальное)
        :param end_local: конечное время чтения (локальное)
        :return: массив значений тега
        """
        utc_start = start_local.astimezone(pytz.UTC).replace(tzinfo=None)
        utc_end = end_local.astimezone(pytz.UTC).replace(tzinfo=None)
        ret_val: List[DataDouble] = []
        d = Table('DataDouble')
        q = (self._query.from_(d)
             .where((d.IdTagDef == Parameter('%s'))
                    & (d.TimeWrite[
                       ToTicks(self._schema, Parameter('%s')):ToTicks(self._schema, Parameter('%s'))]))
             .orderby(d.TimeWrite, order=Order.asc)
             .select(d.IdTagDef, d.Data, ToDateTime2(self._schema, d.TimeWrite, alias='TimeWrite'), d.QSlim)
             )
        sql = q.get_sql()
        self._logger.debug(f'SQL: {sql} PARAMS: tag_id:{tag_id}, utc_start={utc_start}, utc_end={utc_end}')
        try:
            result = self._engine_data.execute(sql, tag_id, utc_start, utc_end)
            for row in result:
                data = DataDouble(
                    tag_id, row['Data'],
                    datetime.strptime(row['TimeWrite'][:23], self.DATETIME_FORMAT_F).replace(
                        tzinfo=pytz.UTC).astimezone(settings.TIME_ZONE),
                    row['QSlim'])
                ret_val.append(data)
        except Exception as e:
            self._logger.error(e)
        return ret_val
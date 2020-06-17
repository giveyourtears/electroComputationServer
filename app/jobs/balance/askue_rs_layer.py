from logging import Logger
from app.models.askue import DataDouble
from pypika import Table, PostgreSQLQuery as Q, Order, Parameter  # type: ignore
from pendulum import datetime as penddt
import pytz
from typing import List
from app.models.askue.askue_rs import engine_rs_data, engine_rs_main
from pypika.functions import DistinctOptionFunction
from app.jobs.balance.askue_layer_base import AskueLayerBase
from app.models.askue.askue_reg import DATETIME_FORMAT as DF_PG
from app.storage import settings


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


class DalRs(AskueLayerBase):
    """
    Класс DAL работы с БД АСКУЭ объектов распределительной сети
    """
    def __init__(self, logger: Logger):
        self._schema = 'public'
        self.DATETIME_FORMAT = DF_PG
        super().__init__(logger, engine_rs_main, engine_rs_data, Q)

    def read_rs_values(self, tag_id: int, start_local: penddt, end_local: penddt) -> List[DataDouble]:
        """
        Выполняет чтение всех точек учета
        :return: массив точек учета
        """
        d = Table('DataDouble')
        utc_start = start_local.astimezone(pytz.UTC).replace(tzinfo=None)
        utc_end = end_local.astimezone(pytz.UTC).replace(tzinfo=None)

        ret_val: List[DataDouble] = []
        q = (Q.from_(d)
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
                    tag_id,
                    row['Data'],
                    row['TimeWrite'].replace(
                        tzinfo=pytz.UTC).astimezone(settings.TIME_ZONE),
                    row['QSlim'])
                ret_val.append(data)
        except Exception as e:
            self._logger.error(e)
        return ret_val

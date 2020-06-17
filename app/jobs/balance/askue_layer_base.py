from sqlalchemy.engine import Engine
from logging import Logger
from typing import List, Union
from datetime import datetime

from pypika import Query, MSSQLQuery, Table, Order, Parameter, AliasedQuery, JoinType, Case  # type: ignore
from pypika.functions import DistinctOptionFunction, Max, Cast  # type: ignore
import pytz

from app.models.askue import DataDouble, AccountPoint
from app.models.askue.askue_reg import DATETIME_FORMAT_F as DF_MSSQL
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


class AskueLayerBase:
    """
    Базовый класс DAL работы с БД eMax
    """

    def __init__(self, logger: Logger, engine_main: Engine, engine_data: Engine, query: Query):
        self._logger = logger
        self._engine_main = engine_main
        self._engine_data = engine_data
        self._query = query
        self._schema = 'public'
        self._FALSE_: Union[bool, int] = False
        self.__needRvCast = False
        if query == MSSQLQuery:
            self._schema = 'dbo'
            self.DATETIME_FORMAT_F = DF_MSSQL
            self._FALSE_ = 0
            self.__needRvCast = True

    def read_id_component_type(self) -> int:
        """
            Выполняет чтение id типа компонента
            :return: id типа
        """
        t = Table('ComponentType', alias='t')
        q = (self._query.from_(t).where(t.Guid == 'est.by:ElectroPassport').select(t.Id))
        sql = q.get_sql()
        ret_value: int = 0
        try:
            self._logger.debug(f'SQL: {sql}')
            result = self._engine_main.execute(sql)
            for row in result:
                ret_value = row[0]
        except Exception as e:
            self._logger.error(e)
        return ret_value

    def read_serial_id(self, find_id: int) -> int:
        ds = Table('DataString', alias='ds')
        query = (Query.from_(ds)
                 .select(ds.Data, Max(ds.TimeWrite))
                 .where(ds.IdTagDef == find_id)
                 .groupby(ds.Data)
                 .limit(1)
                 )
        sql = query.get_sql()
        ret_value: int = 0
        try:
            self._logger.debug(f'SQL: {sql}')
            result = self._engine_data.execute(sql)
            for row in result:
                ret_value = row[0]
        except Exception as e:
            self._logger.error(e)
        return ret_value

    def read_account_points(self, rv: int, id_component_type: int) -> List[AccountPoint]:
        """
        Выполняет чтение всех точек учета
        :return: массив точек учета
        """
        a = Table('AccountPoint', alias='a')
        t = Table('Tag', alias='t')
        n = Table('Node', alias='n')
        n2 = Table('Node', alias='n2')
        n3 = Table('Node', alias='n3')
        n4 = Table('Node', alias='n4')
        p = Table('ObjPassport', alias='p')
        c = Table('ComponentType', alias='c')
        s = Table('DataString', alias='c')
        sub_query = (Query.from_(a)
                     .join(t, how=JoinType.inner).on(a.Id == t.AccountId)
                     .join(n, how=JoinType.inner).on(a.DriverId == n.Id)
                     .join(c, how=JoinType.inner).on(n.IdComponentType == c.Id)
                     .join(n2, how=JoinType.inner).on(a.Id == n2.Id)
                     .join(n3, how=JoinType.inner).on((n2.IdOwn == n3.IdOwn) & (n3.BrowseName == 'Diagnostic'))
                     .join(n4, how=JoinType.inner).on((n3.Id == n4.IdOwn) & (n4.BrowseName == 'SerialNumber'))
                     .where((a.Del == self._FALSE_) & (t.TagCategory == 'CounterAplus') & (t.TagName == 'Day1') &
                            (a.Rv > 0)))
        if self.__needRvCast:
            sub_query = sub_query.select(a.Id, a.DisplayName, t.IdTagDef, a.DriverId, c.Guid,
                                         Cast(a.Rv, 'BIGINT', 'Rv'), n3.BrowseName, n4.Id.as_('serial_num'))
        else:
            sub_query = sub_query.select(a.Id, a.DisplayName, t.IdTagDef, a.DriverId, c.Guid, a.Rv, n3.BrowseName,
                                         n4.Id.as_('serial_num'))

        ap = AliasedQuery("ap")
        query = (Query
                 .select(ap.Id, ap.DisplayName, ap.IdTagDef, ap.Rv, p.PostIndex, p.FlatS, p.Flat, p.Region, p.Country,
                         ap.serial_num,
                         Case()
                         .when(ap.Guid == 'est.by:Bus.GranDrvClientImpl', 'СС-301')
                         .when(ap.Guid == 'est.by:Bus.Gran101DrvClientImpl', 'СС-101')
                         .when(ap.Guid == 'est.by:Bus.EmeraDrvClientImpl', 'СЕ-102')
                         .else_("UNKNOWN").as_('Driver')
                         )
                 .with_(sub_query, "ap")
                 .from_(ap)
                 .join(n, how=JoinType.left).on((n.IdOwn == ap.Id) & (n.IdComponentType == id_component_type))
                 .join(p, how=JoinType.left).on(n.Id == p.Id))

        sql = query.get_sql()
        ret_val: List[AccountPoint] = []
        try:
            self._logger.debug(f'SQL: {sql}')
            result = self._engine_main.execute(sql)
            for row in result:
                data = AccountPoint(row['Id'], row['DisplayName'], row['IdTagDef'], row['PostIndex'],
                                    row['FlatS'], row['Flat'], row['Region'], row['Country'], row['serial_num'], row['Driver'], row['Rv'])
                ret_val.append(data)
        except Exception as e:
            self._logger.error(e)
        return ret_val



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

    def read_points(self) -> List[AccountPoint]:
        """
        Выполняет чтение всех точек учета
        :return: массив точек учета
        """
        p = Table('AccountPointList', alias='p')
        t = Table('Tag', alias='t')
        q = (self._query.from_(p)
             .join(t)
             .on(p.Id == t.AccountId)
             .select(p.Id, p.DisplayName, t.IdTagDef, p.Rv)
             .where((p.Del == self._FALSE_) & (t.TagCategory == 'CounterAplus') & (t.TagName == 'Day1'))
             )

        sql = q.get_sql()

        ret_val: List[AccountPoint] = []
        try:
            self._logger.debug(f'SQL: {sql}')
            result = self._engine_main.execute(sql)
            for row in result:
                data = AccountPoint(row['Id'], row['DisplayName'], row['IdTagDef'], row['Rv'])
                ret_val.append(data)
        except Exception as e:
            self._logger.error(e)
        return ret_val

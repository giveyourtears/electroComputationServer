from logging import Logger
from typing import List
from pypika import Table  # type: ignore
from pypika import PostgreSQLQuery as Q
from app.models.mart import engine_mart
from app.models.askue import AccountPoint
from app.models.mart import RegPointModel, RsPointModel, BalanceModel, BalanceRegModel
from sqlalchemy.engine import Transaction
from pypika.functions import Max  # type: ignore


class DalMart:
    """
    Класс DAL работы с БД Data Mart объектов
    """

    def __init__(self, logger: Logger):
        self._logger = logger

    def get_max_rv_point_list(self, point_table: str) -> int:
        rv = 0
        try:
            p = Table(point_table)
            q = (Q.from_(p)
                 .select(Max(p.rv)))
            sql = q.get_sql()
            self._logger.debug(f'SQL: {sql}')
            rv = engine_mart.scalar(sql)
            if rv is None:
                rv = 0
        except Exception as e:
            self._logger.error(e)
        return rv

    def insert_points(self, points: List[AccountPoint], dest_table: str) -> None:
        con = engine_mart.connect()
        self._logger.debug(f'DalMart.insert_point() dest_table:{dest_table}')
        if dest_table == 'askue_reg_point':
            data_result: List[RegPointModel] = []
            tran: Transaction = con.begin()
            try:
                for p in points:
                    reg_string = p.DisplayName.split('\\')
                    if len(reg_string) < 4:
                        self._logger.warning(f"Имя объекта ({p.DisplayName}) не соответствует формату")
                        continue
                    reg_object = RegPointModel(id_point=p.Id, display_name=p.DisplayName, res=reg_string[0],
                                               fes=reg_string[1], ps=reg_string[2], vl=reg_string[3], rv=p.Rv)
                    data_result.append(reg_object)
            except Exception as e:
                self._logger.error(f'convert to model failed {e}')

            try:
                for elem in data_result:
                    d = Table(dest_table)
                    q = Q.into(d).insert(elem.Id, elem.DisplayName, elem.Res, elem.Fes, elem.Ps, elem.Vl, elem.Rv) \
                        .on_conflict(d.id) \
                        .do_update(d.object_name, elem.DisplayName) \
                        .do_update(d.fes, elem.Fes) \
                        .do_update(d.res, elem.Res) \
                        .do_update(d.ps, elem.Ps) \
                        .do_update(d.vl, elem.Vl) \
                        .do_update(d.rv, elem.Rv)
                    sql = q.get_sql()
                    self._logger.debug(f'SQL: {sql}')
                    con.execute(sql)
                tran.commit()
            except Exception as e:
                self._logger.error(f'DalMart.insert_point() {e}')
                tran.rollback()
        else:
            data_result: List[RsPointModel] = []
            tran: Transaction = con.begin()
            try:
                for p in points:
                    rs_string = p.DisplayName.split('\\')
                    if len(rs_string) < 6:
                        self._logger.warning(f"Имя объекта ({p.DisplayName}) не соответствует формату")
                        continue
                    rs_object = RsPointModel(id_point=p.Id, display_name=p.DisplayName, res=rs_string[0],
                                             fes=rs_string[1], ps=rs_string[2], vl=rs_string[3], tp=rs_string[4],
                                             sch=rs_string[5], ktt=p.Ktt, str_ra=p.Str_ra, rxx=p.Rxx, region=p.Locality,
                                             number_point=p.Number_point, driver=p.Driver, rv=p.Rv, country=p.Country)
                    data_result.append(rs_object)
            except Exception as e:
                self._logger.error(f'convert to model failed {e}')
            try:
                for elem in data_result:
                    d = Table(dest_table)
                    q = Q.into(d).insert(elem.Id, elem.DisplayName, elem.Res, elem.Fes, elem.Ps, elem.Vl,
                                         elem.Tp, elem.Sch, elem.Rv, elem.Str_ra, elem.Rxx, elem.Ktt, elem.Region,
                                         elem.Number_point, elem.Driver, elem.Country) \
                        .on_conflict(d.id) \
                        .do_update(d.object_name, elem.DisplayName) \
                        .do_update(d.fes, elem.Fes) \
                        .do_update(d.res, elem.Res) \
                        .do_update(d.ps, elem.Ps) \
                        .do_update(d.vl, elem.Vl) \
                        .do_update(d.tp, elem.Tp) \
                        .do_update(d.sch, elem.Sch) \
                        .do_update(d.rv, elem.Rv) \
                        .do_update(d.str_ra, elem.Str_ra) \
                        .do_update(d.rxx, elem.Rxx) \
                        .do_update(d.ktt, elem.Ktt) \
                        .do_update(d.locality, elem.Region) \
                        .do_update(d.number_point, elem.Number_point) \
                        .do_update(d.driver, elem.Driver) \
                        .do_update(d.country, elem.Country)
                    sql = q.get_sql()
                    self._logger.debug(f'SQL: {sql}')
                    con.execute(sql)
                tran.commit()
            except Exception as e:
                self._logger.error(f'DalMart.insert_point() {e}')
                tran.rollback()

    def read_rs_points(self) -> List[RsPointModel]:
        """
        Выполняет чтение всех точек учета распределительных сетей
        :return: массив точек учета
        """
        p = Table('askue_rs_point', alias='p')
        q = (Q.from_(p)
             .select(p.id, p.object_name, p.fes, p.res, p.ps, p.vl, p.tp, p.sch, p.rv, p.str_ra, p.rxx, p.ktt,
                     p.locality, p.number_point, p.driver, p.country))
        sql_query = q.get_sql()

        return_values: List[RsPointModel] = []
        try:
            self._logger.debug(f'SQL: {sql_query}')
            result = engine_mart.execute(sql_query)
            for row in result:
                data = RsPointModel(id_point=row['id'], display_name=row['object_name'], fes=row['fes'], res=row['res'],
                                    ps=row['ps'], vl=row['vl'], tp=row['tp'], sch=row['sch'], rv=row['rv'],
                                    str_ra=row['str_ra'], rxx=row['rxx'], ktt=row['ktt'], region=row['locality'],
                                    number_point=row['number_point'], driver=row['driver'], country=row['country'])
                return_values.append(data)
        except Exception as e:
            self._logger.error(e)
        return return_values

    def read_reg_points(self) -> List[RegPointModel]:
        """
        Выполняет чтение всех точек учета распределительных сетей
        :return: массив точек учета
        """
        p = Table('askue_reg_point', alias='p')
        q = (Q.from_(p)
             .select(p.id, p.object_name, p.fes, p.res, p.ps, p.vl, p.rv))
        sql_query = q.get_sql()

        return_values: List[RegPointModel] = []
        try:
            self._logger.debug(f'SQL: {sql_query}')
            result = engine_mart.execute(sql_query)
            for row in result:
                data = RegPointModel(row['id'], row['object_name'], row['fes'], row['res'], row['ps'], row['vl'],
                                     row['rv'])
                return_values.append(data)
        except Exception as e:
            self._logger.error(e)
        return return_values

    def insert_balance_calc(self, points: List[BalanceModel]):
        """
        Выполняет добавление всех рассчетов в базу данных
        """
        con = engine_mart.connect()
        self._logger.debug("insert_balance_calc()... start")
        tran: Transaction = con.begin()
        try:
            for elem in points:
                d = Table('calc_balance')
                q = Q.into(d).insert(elem.Id, elem.Id_tu, elem.Dtp, elem.Locality, elem.NameOfAccountingPoint,
                                     elem.STrRa,
                                     elem.Pxx,
                                     elem.LossXX, elem.Ktt, elem.HeadOfCounter, elem.StartPeriod,
                                     elem.QSlim, elem.Time_Start_Write, elem.Country, elem.Driver) \
                    .on_conflict(d.id) \
                    .do_update(d.id_tu, elem.Id_tu) \
                    .do_update(d.dtp, elem.Dtp) \
                    .do_update(d.locality, elem.Locality) \
                    .do_update(d.name_of_accounting_point, elem.NameOfAccountingPoint) \
                    .do_update(d.str_ra, elem.STrRa) \
                    .do_update(d.pxx, elem.Pxx) \
                    .do_update(d.loss_xx, elem.LossXX) \
                    .do_update(d.ktt, elem.Ktt) \
                    .do_update(d.head_of_counter, elem.HeadOfCounter) \
                    .do_update(d.start_period, elem.StartPeriod) \
                    .do_update(d.q_slim, elem.QSlim) \
                    .do_update(d.time_start_write, elem.Time_Start_Write) \
                    .do_update(d.country, elem.Country) \
                    .do_update(d.driver, elem.Driver)
                sql = q.get_sql()
                self._logger.debug(f'SQL: {sql}')
                con.execute(sql)
            tran.commit()
        except Exception as e:
            self._logger.error(f'DalMart.insert_balance_calc() {e}')
            tran.rollback()

    def insert_balance_reg_calc(self, points: List[BalanceRegModel]):
        """
        Выполняет добавление всех рассчетов в базу данных
        """
        con = engine_mart.connect()
        self._logger.debug("insert_balance_calc()... start")
        tran: Transaction = con.begin()
        try:
            for elem in points:
                d = Table('calc_reg_balance')
                q = Q.into(d).insert(elem.Id, elem.Id_tu, elem.StartPeriod, elem.Time_Start_Write) \
                    .on_conflict(d.id) \
                    .do_update(d.id_tu, elem.Id_tu) \
                    .do_update(d.start_period, elem.StartPeriod) \
                    .do_update(d.time_start_write, elem.Time_Start_Write)
                sql = q.get_sql()
                self._logger.debug(f'SQL: {sql}')
                con.execute(sql)
            tran.commit()
        except Exception as e:
            self._logger.error(f'DalMart.insert_balance_reg_calc() {e}')
            tran.rollback()
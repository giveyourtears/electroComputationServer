import logging
from typing import List, Dict, Optional
from sqlalchemy.engine import Engine
from app.jobs.balance.askue_layer_base import AskueLayerBase
from app.jobs.balance import DalReg, DalRs, DalMart
from app.models.askue import AccountPoint
import pendulum as pend
from pendulum import DateTime
from app.models.askue import DataDouble
from app.models.mart import RsPointModel, RegPointModel
from app.models.mart import BalanceModel, BalanceRegModel
from app.storage import settings
from datetime import datetime
import pytz
from locale import atof, setlocale, LC_ALL


class BalanceCalc:

    def __init__(self):
        self.__logger = logging.getLogger('BalanceCalc')
        self._dalReg = DalReg(self.__logger)
        self._dalRs = DalRs(self.__logger)
        self._dalMart = DalMart(self.__logger)
    @staticmethod
    def run() -> None:
        calc = BalanceCalc()
        calc.calculate()

    def to_float(self, text: str) -> float:
        try:
            if not text:
                text = 0
                return text
            return atof(text)
        except Exception as e:
            setlocale(LC_ALL, '')
            if text is None:
                text = 0
                return text
            return atof(text)

    def calculate(self) -> None:
        self.__sync_point_list(self._dalReg, 'askue_reg_point')
        self.__sync_point_list(self._dalRs, 'askue_rs_point')
        dict_obj: Dict[int, int] = dict()
        dict_obj_reg: Dict[int, int] = dict()
        id_component_type = self._dalRs.read_id_component_type()
        points: List[AccountPoint] = self._dalRs.read_account_points(0, id_component_type)
        points_reg: List[AccountPoint] = self._dalReg.read_account_points(0, id_component_type)
        for p in points:
            dict_obj[p.CounterAplusId] = p.Id

        for p in points_reg:
            dict_obj_reg[p.CounterAplusId] = p.Id

        self.__calculate_balance(self._dalRs, self._dalMart, dict_obj)
        self.__calculate_balance_reg(self._dalReg, self._dalMart, dict_obj_reg)

    def __sync_point_list(self, askue: AskueLayerBase, dest_table: str) -> None:
        max_rv = self._dalMart.get_max_rv_point_list(dest_table)
        id_component_type = self._dalRs.read_id_component_type()
        point_list: List[AccountPoint] = askue.read_account_points(max_rv, id_component_type)
        for find_id in point_list:
            idxa: int = askue.read_serial_id(find_id.Number_point)
            find_id.Number_point = idxa
        try:
            for p in point_list:
                p.DisplayName = p.DisplayName.replace('!', '')
                p.Rxx = self.to_float(p.Rxx)
                p.Str_ra = self.to_float(p.Str_ra)
                p.Ktt = self.to_float(p.Ktt)
        except Exception as e:
            self.__logger.error("error" + e)
        self._dalMart.insert_points(point_list, dest_table)

    def get_values_from_one_tu(self, key, start, end) -> List[DataDouble]:
        data = self._dalRs.read_rs_values(key, start, end)
        return data

    def get_values_from_one_tu_reg(self, key, start, end) -> List[DataDouble]:
        data = self._dalReg.read_tag_values(key, start, end)
        return data

    def __calculate_balance(self, rs: DalRs, mart: DalMart, dict_obj: Dict[int, int]) -> None:
        """
        Выполняет расчет балансов
        """
        tz = pend.timezone('Europe/Minsk')
        now: DateTime = pend.now(tz)
        end_local: DateTime = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_local = end_local.subtract(days=30)
        try:
            # Словарь по всем точкам и их описаниям
            description_dict = self.create_dict_point_description()
            for id_one_tu in dict_obj.keys():
                dict_point_by_day = self.create_dict_points(id_one_tu, end_local)
                id_tu = dict_obj.get(id_one_tu)
                get_value_for_one_tu: List[DataDouble] = self.get_values_from_one_tu(id_one_tu, start_local, end_local)
                if description_dict.get(id_tu) is None:
                    continue
                else:
                    rs_point: RsPointModel = description_dict.get(id_tu)
                for data_one_tu in get_value_for_one_tu:
                    if dict_point_by_day.get(data_one_tu.TimeWrite, None) is None:
                        continue
                    dict_point_by_day[data_one_tu.TimeWrite] = data_one_tu

                date_array: List[DataDouble] = list(dict_point_by_day.values())
                balance_list: List[BalanceModel] = []
                for elem in date_array:
                    result_id = self.create_id_for_point(elem.IdTagDef, elem.TimeWrite)
                    balance_model = BalanceModel(result_id, rs_point.Id, rs_point.Tp, rs_point.Region,
                                                 rs_point.Country, rs_point.Driver, rs_point.Sch,
                                                 rs_point.Str_ra, rs_point.Rxx, 1.0, rs_point.Ktt,
                                                 rs_point.Number_point,
                                                 elem.Data, elem.QSlim,
                                                 elem.TimeWrite.astimezone(pytz.UTC).replace(tzinfo=None))
                    balance_list.append(balance_model)
                mart.insert_balance_calc(balance_list)
        except Exception as e:
            self.__logger.error(f'__calculate_balance {e}')

    def __calculate_balance_reg(self, rs: DalReg, mart: DalMart, dict_obj: Dict[int, int]) -> None:
        """
        Выполняет расчет балансов
        """
        tz = pend.timezone('Europe/Minsk')
        now: DateTime = pend.now(tz)
        end_local: DateTime = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_local = end_local.subtract(days=30)
        try:
            # Словарь по всем точкам и их описаниям
            description_dict = self.create_dict_reg_point_description()
            for id_one_tu in dict_obj.keys():
                dict_point_by_day = self.create_dict_points(id_one_tu, end_local)
                id_tu = dict_obj.get(id_one_tu)
                get_value_for_one_tu: List[DataDouble] = self.get_values_from_one_tu_reg(id_one_tu, start_local,
                                                                                         end_local)
                if description_dict.get(id_tu) is None:
                    continue
                else:
                    reg_point: RegPointModel = description_dict.get(id_tu)
                for data_one_tu in get_value_for_one_tu:
                    if dict_point_by_day.get(data_one_tu.TimeWrite, None) is None:
                        continue
                    dict_point_by_day[data_one_tu.TimeWrite] = data_one_tu

                date_reg_array: List[DataDouble] = list(dict_point_by_day.values())
                balance_reg_list: List[BalanceRegModel] = []
                for elem in date_reg_array:
                    result_id = self.create_id_for_point(elem.IdTagDef, elem.TimeWrite)
                    balance_reg_model = BalanceRegModel(result_id, reg_point.Id, elem.Data,
                                                        elem.TimeWrite.astimezone(pytz.UTC).replace(tzinfo=None))
                    balance_reg_list.append(balance_reg_model)
                mart.insert_balance_reg_calc(balance_reg_list)
        except Exception as e:
            self.__logger.error(f'__calculate_balance {e}')

    def create_dict_points(self, id: int, end_time: DateTime) -> Dict[datetime, DataDouble]:
        point_dict_by_day: Dict[datetime, DataDouble] = dict()
        try:
            for i in range(0, settings.BALANCE_RECALC_DEEP):
                point_dict_by_day[end_time] = DataDouble(id, 0.0, end_time, 0)
                end_time = end_time.subtract(days=1)
        except Exception as e:
            self.__logger.error(f'_create_dict_points {e}')
        return point_dict_by_day

    def create_dict_point_description(self) -> Dict[int, RsPointModel]:
        point_description: Dict[int, RsPointModel] = dict()
        try:
            dm_elements: List[RsPointModel] = self._dalMart.read_rs_points()
            for i in dm_elements:
                point_description[i.Id] = i
        except Exception as e:
            self.__logger.error(f'_create_dict_point_description {e}')
        return point_description

    def create_dict_reg_point_description(self) -> Dict[int, RegPointModel]:
        point_reg_description: Dict[int, RegPointModel] = dict()
        try:
            dm_elements: List[RegPointModel] = self._dalMart.read_reg_points()
            for i in dm_elements:
                point_reg_description[i.Id] = i
        except Exception as e:
            self.__logger.error(f'_create_dict_reg_point_description {e}')
        return point_reg_description

    def create_id_for_point(self, id: int, time: datetime) -> str:
        result_id = str(id) + '_' + str(time.year) + '-' + str(time.month) + '-' + str(time.day)
        return result_id

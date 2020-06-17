from dataclasses import dataclass


@dataclass
class BalanceRegModel():
    """
    Класс описания таблицы расчета балансов
    """
    """Идентефикатор"""
    Id: str
    """Идентефикатор ТУ"""
    Id_tu: int
    """Начало периода"""
    StartPeriod: float
    """Начальное время записи"""
    Time_Start_Write: str

    def __init__(self, id, id_tu, startperiod, time_start_write):
        self.Id = id
        self.Id_tu = id_tu
        self.StartPeriod = startperiod
        self.Time_Start_Write = time_start_write

    def __repr__(self):
        return 'Id: {}, Id_tu:{}, StartPeriod:{}, Time_Start_Write:{} '\
                .format(self.Id, self.Id_tu, self.StartPeriod, self.Time_Start_Write)






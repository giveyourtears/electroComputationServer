from dataclasses import dataclass


@dataclass
class BalanceModel():
    """
    Класс описания таблицы расчета балансов
    """
    """Идентефикатор"""
    Id: str
    """Идентефикатор ТУ"""
    Id_tu: int
    """Диспетчерский номер ТП"""
    Dtp: str
    """Населенный пункт"""
    Locality: str
    """Наименование точки учета"""
    NameOfAccountingPoint: str
    """S тр-ра, кВА"""
    STrRa: int
    """Pхх"""
    Pxx: float
    """Потери ХХ за период, кВт*ч"""
    LossXX: float
    """Ktt"""
    Ktt: int
    """Зав.№ счетчика"""
    HeadOfCounter: int
    """Начало периода"""
    StartPeriod: float
    """Расход за период"""
    QSlim: int
    """Начальное время записи"""
    Time_Start_Write: str
    """Сельсовет"""
    Country: str
    """Тип точки"""
    Driver: str

    def __init__(self, id, id_tu, dtp, locality, country, driver, name_of_accounting_point, str_ra, pxx, loss_xx, ktt, head_of_counter,
                 start_period, q_slim, time_start_write):
        self.Id = id
        self.Id_tu = id_tu
        self.Dtp = dtp
        self.Locality = locality
        self.Country = country
        self.Driver = driver
        self.NameOfAccountingPoint = name_of_accounting_point
        self.STrRa = str_ra
        self.Pxx = pxx
        self.LossXX = loss_xx
        self.Ktt = ktt
        self.HeadOfCounter = head_of_counter
        self.StartPeriod = start_period
        self.QSlim = q_slim
        self.Time_Start_Write = time_start_write

    def __repr__(self):
        return 'Id: {}, Id_tu:{}, Dtp:{}, Locality:{}, Country:{}, Driver: {}, NameOfAccountingPoint:{}, STrRa:{}, ' \
               'Pxx:{}, LossXX:{}, Ktt:{}, HeadOfCounter:{}, StartPeriod:{}, QSlim:{}, Time_Start_Write:{} '\
                .format(self.Id, self.Id_tu, self.Dtp, self.Locality, self.Country, self.Driver,
                        self.NameOfAccountingPoint, self.STrRa, self.Pxx, self.LossXX, self.Ktt, self.HeadOfCounter,
                        self.StartPeriod, self.QSlim, self.Time_Start_Write)






from dataclasses import dataclass
from sqlalchemy import VARBINARY


@dataclass
class AccountPoint:
    """
    Класс описания точки учета
    """
    """Идентификатор ТУ"""
    Id: int
    """Наименование ТУ"""
    DisplayName: str
    """Идентификатор тега счетчика энергии A+"""
    CounterAplusId: int
    """Rxx"""
    Rxx: float
    """S tr-ra"""
    Str_ra: float
    """Ktt"""
    Ktt: float
    """Населенный пункт"""
    Locality: str
    """Сельсовет"""
    Country: str
    """N* Счетчика"""
    Number_point: int
    """Драйвер"""
    Driver: str
    """Версия записи"""
    Rv: int

    def __repr__(self):
        return 'Id:{}, DisplayName:{}, CounterAplusId:{}'.format(self.Id, self.DisplayName, self.CounterAplusId)
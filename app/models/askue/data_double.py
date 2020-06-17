from dataclasses import dataclass
from datetime import datetime


@dataclass
class DataDouble:
    """
    Класс единичного значения тега
    """
    """Идентификатор тега"""
    IdTagDef: int
    """Значение"""
    Data: float
    """Время значения"""
    TimeWrite: datetime
    """Качество данных"""
    QSlim: int
    def __repr__(self):
        return 'Data:{}, TimeWrite:{}, QSlim:{}'.format(self.Data, self.TimeWrite, self.QSlim)

# class DataDouble:
#     """
#     Класс описания единичного значения типа double
#     """
#     __tablename__ = 'DataDouble'
#     """
#     Идентификатор тега
#     """
#     IdTagDef = Column(Integer)
#     """
#     Значение тега
#     """
#     Data = Column(Float)
#     """
#     Время, на которое приходится значение
#     """
#     TimeWrite = Column(DateTime)
#     """
#     Качество данных
#     """
#     QSlim = Column(Integer)
#
#     def __repr__(self):
#         return 'Data:{}, TimeWrite:{}, QSlim:{}'.format(self.Data, self.TimeWrite, self.QSlim)

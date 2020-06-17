from sqlalchemy import Column, String, Integer, Float, DateTime
from app.models.mart.core import MartBase


class BalanceRegTable(MartBase):
    __tablename__ = 'calc_reg_balance'
    id = Column(String(100), primary_key=True)
    id_tu = Column(Integer, nullable=False)
    start_period = Column(Float, nullable=False)
    time_start_write = Column(DateTime, nullable=False)

    def __repr__(self):
        return 'id: {}'.format(self.id)


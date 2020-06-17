from sqlalchemy import Column, String, Integer, Float, DateTime
from app.models.mart.core import MartBase


class BalanceTable(MartBase):
    __tablename__ = 'calc_balance'
    id = Column(String(100), primary_key=True, nullable=False)
    id_tu = Column(Integer, nullable=False)
    dtp = Column(String(10), nullable=False)
    locality = Column(String(40), nullable=False)
    country = Column(String())
    driver = Column(String(50))
    name_of_accounting_point = Column(String(40), nullable=False)
    str_ra = Column(Integer, nullable=False)
    pxx = Column(Float, nullable=False)
    loss_xx = Column(Float, nullable=False)
    ktt = Column(Integer, nullable=False)
    head_of_counter = Column(Integer, nullable=False)
    start_period = Column(Float, nullable=False)
    q_slim = Column(Integer, nullable=False)
    time_start_write = Column(DateTime, nullable=False)

    def __repr__(self):
        return 'id: {}, object_name: {}'.format(self.id, self.name_of_accounting_point)


from sqlalchemy import Column, String, Integer, func, BigInteger
from app.models.mart.core import MartBase


class AskueRegPoint(MartBase):
    __tablename__ = 'askue_reg_point'
    id = Column(Integer, primary_key=True)
    object_name = Column(String(512), nullable=False, index=True)
    fes = Column(String(25), nullable=False)
    res = Column(String(50), nullable=False)
    ps = Column(String(50), nullable=False)
    vl = Column(String(50), nullable=False)
    rv = Column(BigInteger, nullable=False, index=True)

    def __repr__(self):
        return 'id: {}, object_name: {}'.format(self.id, self.object_name)


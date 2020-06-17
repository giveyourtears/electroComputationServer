from sqlalchemy import Column, String, Integer, BigInteger, Float
from app.models.mart.core import MartBase


class AskueRsPoint(MartBase):
    __tablename__ = 'askue_rs_point'
    id = Column(Integer, primary_key=True)
    object_name = Column(String(512), nullable=False, index=True)
    fes = Column(String(25), nullable=False)
    res = Column(String(50), nullable=False)
    ps = Column(String(50), nullable=False)
    vl = Column(String(50), nullable=False)
    tp = Column(String(50), nullable=False)
    sch = Column(String(50), nullable=False)
    rv = Column(BigInteger, nullable=False, index=True)
    str_ra = Column(Float, nullable=False)
    rxx = Column(Float, nullable=False)
    ktt = Column(Float, nullable=False)
    locality = Column(String(100), nullable=False)
    country = Column(String())
    number_point = Column(Integer, nullable=False)
    driver = Column(String(50), nullable=False)

    def __repr__(self):
        return 'id: {}, object_name: {}'.format(self.id, self.object_name)


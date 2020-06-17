from app.models.mart.regpointmodel import RegPointModel


class RsPointModel(RegPointModel):
    """КТП"""
    Tp: str
    """Счетчики"""
    Sch: str
    """Str_ra"""
    Str_ra: float
    """Rxx"""
    Rxx: float
    """Ктт"""
    Ktt: float
    """Населенный пункт"""
    Region: str
    """Сельсовет"""
    Country: str
    """N* Счетчика"""
    Number_point: int
    """Драйвер"""
    Driver: str

    def __init__(self, id_point, display_name, fes, res, ps, vl, tp, sch, rv, ktt, str_ra, rxx, region, country,
                 number_point, driver):
        self.Id = id_point
        self.DisplayName = display_name
        self.Fes = fes
        self.Res = res
        self.Ps = ps
        self.Vl = vl
        self.Tp = tp
        self.Sch = sch
        self.Rv = rv
        self.Str_ra = str_ra
        self.Rxx = rxx
        self.Ktt = ktt
        self.Region = region
        self.Country = country
        self.Number_point = number_point
        self.Driver = driver

    def __repr__(self):
        return 'Id:{}, DisplayName:{}, Fes:{}, Res:{}, Ps:{}, Vl:{}, Tp:{}, Sch:{}, Rv:{}, Str_ra:{},' \
               'Rxx:{}, Ktt:{}, Region:{}, Country:{}, Number_point:{}, Driver:{}'.format(
            self.Id, self.DisplayName, self.Fes, self.Res, self.Ps, self.Vl, self.Tp, self.Sch, self.Rv, self.Str_ra,
            self.Rxx, self.Ktt, self.Region, self.Country, self.Number_point, self.Driver)

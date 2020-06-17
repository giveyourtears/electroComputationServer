from dataclasses import dataclass


@dataclass
class RegPointModel:
    """
    Класс описания точки учета витрины данных
    """
    """Идентификатор ТУ"""
    Id: int
    """Наименование ТУ"""
    DisplayName: str
    """Версия записи"""
    Rv: int
    """Наименование главной электрической сети"""
    Fes: str
    """Районные электрические сети"""
    Res: str
    """Подстанции"""
    Ps: str
    """Распределители сети"""
    Vl: str

    def __init__(self, id_point, display_name, rv, fes, res, ps, vl):
        self.Id = id_point
        self.DisplayName = display_name
        self.Rv = rv
        self.Fes = fes
        self.Res = res
        self.Ps = ps
        self.Vl = vl

    def __repr__(self):
        return 'Id:{}, DisplayName:{}, Rv:{}, Fes:{}, Res:{}, Ps:{}, Vl:{}'.format(
            self.Id, self.DisplayName, self.Rv, self.Fes, self.Res, self.Ps, self.Vl)






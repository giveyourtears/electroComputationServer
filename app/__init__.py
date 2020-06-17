import schedule  # type: ignore
from time import sleep, ctime
import threading
from typing import Callable
from app.decorators import catch_exceptions, with_logging
from app.jobs.balance.balance_calc import BalanceCalc
from app.storage import settings


class Application:

    def _init_schedules(self) -> None:
        # Все расписания реристрируются сдесь
        calc = BalanceCalc()
        calc.calculate()
        # Пример использования
        #schedule.every(1).seconds.do(Application.run_job, self.sample)

        for t in settings.SCHEDULE_BALANS:
            schedule.every().day.at(t).do(Application.run_job, BalanceCalc.run)

    @staticmethod
    def run() -> None:
        # Запускает цикл обработки заданий
        instance = Application()
        instance._init_schedules()
        while 1:
            schedule.run_pending()
            sleep(1)

    @staticmethod
    def run_job(job_func: Callable) -> None:
        """
        Функция запуска задания в отдельном потоке
        :param job_func: функция задания
        """
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

    # @catch_exceptions(cancel_on_failure=False)
    # @with_logging
    # def sample(self):
    #     print("I'm running on thread %s" % threading.current_thread())


def main() -> None:
    Application.run()

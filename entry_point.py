import os
from logging.handlers import TimedRotatingFileHandler
import logging

from app.storage import settings
from app import Application


def __make_dir(path: str):
    if os.path.isdir(path):
        return
    os.mkdir(path)


def __check_logs_dir():
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, 'app')
    __make_dir(path)
    path = os.path.join(path, 'storage')
    __make_dir(path)
    path = os.path.join(path, 'logs')
    __make_dir(path)


def __init_logging():
    __check_logs_dir()
    handler = TimedRotatingFileHandler(
        settings.LOGGING['file_name'],
        when="d",
        interval=1,
        backupCount=settings.LOGGING['backupCount']
    )
    handler.setFormatter(logging.Formatter(settings.LOGGING['format']))
    root = logging.getLogger()
    root.setLevel(settings.LOGGING['level'])
    root.addHandler(handler)


__init_logging()


def main() -> None:
    Application.run()


if __name__ == "__main__":
    logging.info('Запуск программы')
    main()


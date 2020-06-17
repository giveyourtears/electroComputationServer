import functools
import schedule  # type: ignore


def catch_exceptions(cancel_on_failure=False):
    """
    Функция задания, помеченная этим декоратором, не вызывает прерывание
    основного потока программы. Любая ошибка выполнения будет подавлена.
    Выполнение задания будет прервано.
    :param cancel_on_failure: если параметр установлен в True - задание, при
    выполнении которого произошла ошибка завершается с признаком отмены
    :return: результат выполнения задания
    """

    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob

        return wrapper

    return catch_exceptions_decorator


def with_logging(func):
    """
    Декоратор выполняет вывод сообщений о запуске и
    завершении задания
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
        return result

    return wrapper

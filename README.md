## Планировщик заданий

В качестве планировщика выполнения заданий используется:

https://pypi.org/project/schedule/

Документация:

https://schedule.readthedocs.io/en/stable/

## Построитель запросов

В качестве построителя запросов используется:

https://pypi.org/project/PyPika/

Документация:

https://pypika.readthedocs.io/en/latest/

## Разработка

В ОС разработки должна существовать переменная окружения
```
DEV_PG_HOST=XX.XX.XX.XX
``` 

где XX.XX.XX.XX - является реальным IP-адресом компьютера разработчика

## Создание исполняемого модуля 
```
pyinstaller cli.spec
```

## Шпаргалка по Alembic

* создать миграцию
```
alembic revision -m "create account table"
```
* создать миграцию с автогенерацией кода
```
alembic revision --autogenerate -m "create account table"
```
* выполнить все миграции
```
alembic upgrade head
```
* откатить миграцию до down_revision
```
alembic downgrade <down_revision>
```



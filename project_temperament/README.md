# project_temperament
# Игровая психодиагностика темперамента (методика Айзенка) в формате квеста "Остров"
https://github.com/terenteva-aida/python-2026.git

Документация:
flask: https://flask.palletsprojects.com/en/stable/quickstart/
psycopg: https://wiki.postgresql.org/wiki/Psycopg2_Tutorial

## Стартовая страница (форма)
`GET` /

## Сохранение данных пользователя и старт игры
`POST` /start

## Получение вопроса по номеру (1..7)
`GET` /question/{q_id}

## Прием ответа на вопрос
`POST` /answer/{q_id}

## Подсчет результата и сохранение в БД
`GET` /calculate

## Страница с результатом
`GET` /result
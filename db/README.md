# api_profile
# Приложение реализует endpoint для профиля пользователя
https://github.com/chertkov-vitaliy/api_profile
Документация:
flask:
https://flask.palletsprojects.com/en/stable/quickstart/
psycopg
https://wiki.postgresql.org/wiki/Psycopg2_Tutorial


## Создание аккаунта
`POST` /api/v1/accounts

## Получение аккаунта по ID
`GET` /api/v1/accounts/{id} 

## Обновление аккаунта
`PUT` /api/v1/accounts/{id}

## Удаление аккаунта
`DELETE` /api/v1/accounts/{id}
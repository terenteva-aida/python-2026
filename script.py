# -- Таблица: аккаунт
# CREATE TABLE account (
#     id_account SERIAL PRIMARY KEY,
#     login VARCHAR(255) NOT NULL UNIQUE,
#     pswd VARCHAR(255) NOT NULL,
#     creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
#     last_access_time TIMESTAMP,
#     ip_address INET
# );

# -- Комментарии к таблице и колонкам (документация)
# COMMENT ON COLUMN account.id_account IS 'ID аккаунта (автоинкремент)';
# COMMENT ON COLUMN account.login IS 'Логин пользователя';
# COMMENT ON COLUMN account.pswd IS 'Пароль (рекомендуется хранить хеш)';
# COMMENT ON COLUMN account.creation_date IS 'Дата и время создания аккаунта';
# COMMENT ON COLUMN account.is_blocked IS 'Статус блокировки аккаунта';
# COMMENT ON COLUMN account.last_access_time IS 'Время последнего доступа к аккаунту';
# COMMENT ON COLUMN account.ip_address IS 'IP-адрес (поддерживает ipv4 и ipv6)';

# -- Индекс для быстрого поиска по логину (ускоряет авторизацию)
# CREATE INDEX idx_account_login ON account(login);

# -- Индекс для фильтрации по блокировке и последнему доступу (полезно для очистки старых аккаунтов)
# CREATE INDEX idx_account_last_access ON account(last_access_time);

# -- Индекс для поиска по IP адресу (логирование безопасности)
# CREATE INDEX idx_account_ip ON account(ip_address);

# -- Вставка данных
# INSERT INTO account (login, pswd, creation_date, is_blocked, last_access_time, ip_address)
# VALUES ('joh_doe', 'secure_pas', '2024-01-15 10:30:00', false, '2024-01-15 10:30:00', '10.0.0.1');

# -- Просмотр данных
# SELECT * FROM account;
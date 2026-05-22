# -- Таблица: аккаунт
# CREATE TABLE user_account (
#     id_account SERIAL PRIMARY KEY,
#     login VARCHAR(255) NOT NULL UNIQUE,
#     pswd VARCHAR(255) NOT NULL,
#     creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
#     last_access_time TIMESTAMP,
#     ip_address INET
# );

# COMMENT ON COLUMN user_account.id_account IS 'ID аккаунта (автоинкремент)';
# COMMENT ON COLUMN user_account.login IS 'Логин пользователя';
# COMMENT ON COLUMN user_account.pswd IS 'Пароль (рекомендуется хранить хеш)';
# COMMENT ON COLUMN user_account.creation_date IS 'Дата и время создания аккаунта';
# COMMENT ON COLUMN user_account.is_blocked IS 'Статус блокировки аккаунта';
# COMMENT ON COLUMN user_account.last_access_time IS 'Время последнего доступа к аккаунту';
# COMMENT ON COLUMN user_account.ip_address IS 'IP-адрес (поддерживает ipv4 и ipv6)';

# CREATE INDEX idx_user_account_login ON user_account(login);
# CREATE INDEX idx_user_account_last_access ON user_account(last_access_time);
# CREATE INDEX idx_user_account_ip ON user_account(ip_address);

# INSERT INTO user_account (login, pswd, creation_date, is_blocked, last_access_time, ip_address)
# VALUES ('joh_doe', 'secure_pas', '2024-01-15 10:30:00', false, '2024-01-15 10:30:00', '10.0.0.1');

# SELECT * FROM user_account;
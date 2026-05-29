import os
from markupsafe import escape
from flask import Flask, request, render_template, redirect
from flask import jsonify
from hashlib import md5
import psycopg2
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Мама мыла раму'

def get_db():
  database_url = os.getenv("DATABASE_URL")
  conn = psycopg2.connect(database_url)  
  return conn

@app.route("/")
def hello_world():
    name = "Peter"
    return render_template('hello.html', person=name)

@app.route("/registration",  methods=['GET'])
def registration():
    name = "Peter"
    conn = get_db()
    single_row = ""
    with conn.cursor() as curs:
        try:
           curs.execute("SELECT * from auth.account")
           single_row = curs.fetchall()
        # a more robust way of handling errors
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    print(single_row)
    return render_template('index.html', data=single_row)

    

@app.route('/api/v1/account/<int:id_account>', methods=['PATCH'])
def account_update(id_account):
    conn = get_db()
    with conn.cursor() as curs:
        try:
           curs.execute(f"UPDATE auth.account SET is_blocked=false WHERE id={id_account}")
           conn.commit()
        # a more robust way of handling errors
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    return "ok" , 201


# todo:  Реализуйте данный метод !
@app.route('/api/account/<int:id_account>/', methods=['GET'])
def get_account(id_account):
    conn = get_db()
    with conn.cursor() as curs:
        try:
            curs.execute(f"SELECT id_account, login, creation_date, is_blocked, last_access_time, ip_address FROM auth.account WHERE id_account = {id_account}")
            account = curs.fetchone()
            if account:
                return f"ID: {account[0]}, Login: {account[1]}, Creation date: {account[2]}, Blocked: {account[3]}, Last access: {account[4]}, IP: {account[5]}"
            else:
                return f"Аккаунт с id {id_account} не найден", 404
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Ошибка сервера", 500

    return f'<p>Получить аккаунт по ID:</p>{id_account}'


@app.route('/api/v1/account/<int:id_account>', methods=['GET'] )
def del_account(id_account):
    conn = get_db()
    with conn.cursor() as curs:
        try:
           curs.execute(f"DELETE FROM auth.account WHERE id_account = {id_account}")
           conn.commit()
        # a more robust way of handling errors
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    return redirect('/registration')
    # return f'<p>Удалить аккаунт:</p>{id_account}'

@app.route('/api/v1/account', methods=['POST'])
def post_account():
    login = request.form.get('login')
    pswd = request.form.get('passwd')
    if not login or not pswd:
        return "Логин и пароль обязательны", 400

    hashed = generate_password_hash(pswd)

    conn = get_db()
    with conn.cursor() as curs:
        try:
            curs.execute(f"""INSERT INTO auth.account (ip_address, login, pswd, creation_date, is_blocked, last_access_time)
                             VALUES ('0.0.0.0', '{login}', '{hashed}', CURRENT_TIMESTAMP, false, CURRENT_TIMESTAMP);""")
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Ошибка при регистрации", 500

    return redirect('/profile')   # редирект после регистрации


@app.route('/api/v1/login', methods=['POST'])
def post_login():
    login = request.form.get('login')
    pswd = request.form.get('passwd')
    conn = get_db()
    with conn.cursor() as curs:
        # Получаем хеш пароля из БД для данного логина
        curs.execute(f"SELECT pswd FROM auth.account WHERE login = '{login}'")
        row = curs.fetchone()
    if row and check_password_hash(row[0], pswd):
        return redirect('/profile')
    else:
        return "Неверный логин или пароль", 401


@app.route('/profile')
def profile():
    return "<h1>Добро пожаловать! Вы успешно вошли.</h1><a href='/registration'>Назад</a>"    
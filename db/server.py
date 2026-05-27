import os
from markupsafe import escape
from flask import Flask, request, render_template, redirect
from hashlib import md5
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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
# @app.route('/api/account/<int:id_account>/', methods=['GET'])
# def get_account(id_account):
#     return f'<p>Получить аккаунт по ID:</p>{id_account}'


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


@app.route('/api/v1/account', methods=['POST'] )
def post_account():
    login =  request.form.get('login')
    pswd = request.form.get('passwd')
    conn = get_db()

    with conn.cursor() as curs:
        try:
            
           curs.execute("SELECT version()")
           single_row = curs.fetchone()
           print(f"{single_row}")

           curs.execute( f"""INSERT INTO auth.account ( ip_address, login, pswd, creation_date, is_blocked, last_access_time)
                                  VALUES ('0.0.0.0', '{login}', '{pswd}', CURRENT_TIMESTAMP, false,  CURRENT_TIMESTAMP);""")
           conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

 
    return f"login:{login}  passwd:{pswd}"

    
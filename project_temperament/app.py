import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

# Загрузка переменных из файла .env (конфиденциальные данные не хранятся в коде)
load_dotenv()

# Создаем экземпляр Flask-приложения и секретный ключ для подписи сессионных cookie
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Подключение к базе данных (читает переменную окружения, устанавливает соедение с PostgreSQL, возвращает соединение)
def get_db():
  database_url = os.getenv("DATABASE_URL")
  conn = psycopg2.connect(database_url)  
  return conn

# Главная страница с формой ввода имени, пола, возраста
@app.route('/')
def index():
    return render_template('index.html')

# Сохраняет данные пользователя и начинает игру (сессия)
@app.route('/start', methods=['POST'])
def start():
    name = request.form['name']                                                             # Объект с данными отправленной HTML-формы
    gender = request.form['gender']
    age = request.form.get('age')                                                           # Метод объекта, получающий значение по ключу (по умолчанию - None)
    if age == '':
        age = None
    else:
        age = int(age)

    conn = get_db()
    cur = conn.cursor()                                                                     # Соединение с БД, создание курсора
    cur.execute("""                                                         
        INSERT INTO auth.game_user_results (user_name, gender, age)
        VALUES (%s, %s, %s) RETURNING id
    """, (name, gender, age))
    user_result_id = cur.fetchone()[0]                                                      # Метод курсора, возвращающий данные (строку) в виде кортежа с полем id
    conn.commit()                                                                           # Фиксирует вставку данных
    cur.close()
    conn.close()                                                                            # Закрываем курсор и соединение

    session['user_result_id'] = user_result_id                                              # Сохраняем в сессии идентификатор записи
    session['answers'] = {}                                                                 # Словарь с ответами {episode_id: option_id}  
    return redirect(url_for('question', q_id=1))                                            # Перенаправление на первый вопрос

# Показывает вопрос с номером q_id (декоратор с динамическим параметром <int:q_id>)
@app.route('/question/<int:q_id>')                                          
def question(q_id):
    if 'user_result_id' not in session:                                                     # Проверка сессии
        return redirect(url_for('index'))

    conn = get_db()                                                                         # Соединение с БД, курсор с RealDictCursor (чтобы строки были словарями)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM auth.game_episodes WHERE order_num = %s", (q_id,))           # Ищем запись по номеру вопроса, если нет - возвращаем ошибку
    episode = cur.fetchone()
    if not episode:
        return "Вопрос не найден", 404

    cur.execute("""
        SELECT id, option_text, e_points, n_points
        FROM auth.game_options
        WHERE episode_id = %s
        ORDER BY option_order
    """, (episode['id'],))
    options = cur.fetchall()                                                                # Получаем все варианты ответов для эпизода, возвращает список словарей

    # cur.execute("SELECT gender FROM auth.game_user_results WHERE id = %s", (session['user_result_id'],))
    # user = cur.fetchone()
    # gender = user['gender'] if user else 'не указан'

    cur.close()
    conn.close()

    selected_option = session['answers'].get(str(episode['id']))                            # Восстановление выбранного ответа (для кнопки "Назад") 
    return render_template('question.html',                                                 # Передаем собранные данные в шаблон
                           episode=episode,
                           options=options,
                           q_id=q_id,
                           total_questions=7,
                           selected=selected_option)

# Сохраняет ответ пользователя на текущий вопрос
@app.route('/answer/<int:q_id>', methods=['POST'])
def answer(q_id):
    if 'user_result_id' not in session:
        return redirect(url_for('index'))

    option_id = int(request.form['option'])                                                 # Из формы берем значение поля (id), преобразуем в целое число
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM auth.game_episodes WHERE order_num = %s", (q_id,))          # Сессия хранит ответы по episode_id, по номеру вопроса нужно найти внутренний episode_id
    episode_id = cur.fetchone()[0]
    cur.close()
    conn.close()

    session['answers'][str(episode_id)] = option_id                                         # Кладем в словарь выбранный ответ
    session.modified = True                                                                 # Указываем, что сессия изменилась (меняем вложенный словарь)

    if q_id == 7:                                                                           # Если это последний вопрос, переходим на маршрут calculate
        return redirect(url_for('calculate_result'))
    else:
        return redirect(url_for('question', q_id=q_id + 1))

# Подсчитывает баллы E и N, определяет темперамент, сохраняет в БД
@app.route('/calculate')
def calculate_result():
    if 'user_result_id' not in session:
        return redirect(url_for('index'))

    answers = session.get('answers', {})                                                    # Проверяем сессию, количество ответов
    if len(answers) != 7:
        return "Вы ответили не на все вопросы", 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    e_total = 0
    n_total = 0
    for episode_id_str, option_id in answers.items():                                       # Проходим по всем сохраненным ответам, выбираем баллы, суммируем
        episode_id = int(episode_id_str)
        cur.execute("SELECT e_points, n_points FROM auth.game_options WHERE id = %s", (option_id,))
        points = cur.fetchone()
        e_total += points['e_points']
        n_total += points['n_points']

    if e_total > 0 and n_total <= 0:
        temperament = 'Сангвиник'
    elif e_total > 0 and n_total > 0:
        temperament = 'Холерик'
    elif e_total <= 0 and n_total <= 0:
        temperament = 'Флегматик'
    else:
        temperament = 'Меланхолик'

    cur.execute("""
        UPDATE auth.game_user_results
        SET e_total = %s, n_total = %s, temperament = %s
        WHERE id = %s
    """, (e_total, n_total, temperament, session['user_result_id']))
    conn.commit()                                                                           # Вносим итоговые баллы и темперамент в строку в /start (строка в таблице)

    cur.execute("SELECT user_name, gender, age FROM auth.game_user_results WHERE id = %s",
                (session['user_result_id'],))
    user = cur.fetchone()                                                                   # Достаем имя, пол, возраст
    cur.close()
    conn.close()

    session.pop('answers', None)                                                            # Очистка сессии и подготовка результата
    session['result'] = {
        'name': user['user_name'],
        'gender': user['gender'],
        'age': user['age'],
        'e_total': e_total,
        'n_total': n_total,
        'temperament': temperament
    }

    return redirect(url_for('result'))                                                      # Сохраняем результат в новую переменнную, переходим к следующему маршруту

# Страница с результатом тестирования
@app.route('/result')
def result():
    if 'result' not in session:
        return redirect(url_for('index'))
    return render_template('result.html', result=session['result'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
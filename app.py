from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, flash
from pandas import read_csv, DataFrame
from flask_mail import Mail, Message
from sql.table_methods import *
from datagen import *
import random
import string
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ewhvfgegyVYAQGYVBehg82t7y3882yeuhhddh2yu87u9y8U9YYTu9Y8U98YY8UhUVAGuvhqv'
app.config.from_pyfile('config.cfg')
mail = Mail(app)

generator = Luhn()


def send_email(email, code):
    # функція що потрібна для відправлення
    # повідомлення на пошту користувача
    with app.app_context():
        msg = Message(subject="Confirmation email",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[email])
        msg.body = '''<p>Добрий день! Ось ваш секретний код:</p>
                      <b>{}</b>
                      <p>З повагою,<br>BankApp</p> '''.format(code)
        msg.html = msg.body
        mail.send(msg)


@app.route('/bank/<action>', methods=['GET', 'POST'])
def apiget(action):
    '''
        Функція, що оперує роутами програми
        без зареєстрованого користувача,
        кожний роут переводить користувача
        на відповідну сторінку, також
        присутня сторінка з помилкою
    '''

    if action == 'reg':
        return render_template('reg_page.html')

    elif action == "secret-key":
        return render_template("secret_key.html")

    elif action == "secret-key-approved":
        return render_template("secret_key_approved.html")

    else:
        return render_template("404.html")


@app.route('/', methods=['GET', 'POST'])
def signup():
    '''
        Роут, що переводить на
        головну сторінку програми
    '''
    return render_template('index.html')


@app.route('/reg-in', methods=['GET', 'POST'])
def registration_in():
    '''
        Ця функція відповідає за збір даних
        з флорми та відправлення листа на
        елекронну пошту з згенерованими даними
    '''
    if request.method == 'POST':
        # отримуємо дані з форми
        reg = request.form
        # зберігаємо дані до списку
        row = [str(i) for i in reg.to_dict().values()]
        # якщо тип "картка", то серія паспорту не повертається
        # доводиться вставляти власноруч
        if row[3] == 'card':
            row.insert(4, '')
        # перед тим як продовжувати роботу програми
        # варто перевірити чи вже немає таких даних
        userlogin = UserLogins()
        result = userlogin.get_by_email(email=row[2])
        email = result.first()
        if email is not None:
            flash('User with such credentials is already exists.')
            return redirect(url_for('apiget', action="reg"))

        client = Client()
        result = client.get_by_passid(pass_id=row[4]+row[5])
        ps = result.first()
        if ps is not None:
            flash('User with such credentials is already exists.')
            return redirect(url_for('apiget', action="reg"))

        result = client.get_by_phone(phone=row[9])
        ph = result.first()
        if ph is not None:
            flash('User with such credentials is already exists.')
            return redirect(url_for('apiget', action="reg"))

        result = clt.get_by_ipn(ipn=row[6])
        ipn = result.first()
        if ipn is not None:
            flash('User with such credentials is already exists.')
            return redirect(url_for('apiget', action="reg"))

        # тут звертаємось до функцій генераторів даних
        # та генеруємо ід користувача та секретний ключ
        iban = generator.create_()
        secret_key = get_random_alphanumeric_string(64)
        row.extend([iban, secret_key])  # додаємо їх в список

        # надсилаємо секретний ключ на пошту користувачу
        send_email(email=row[2], code=secret_key)

        # перед збереженням даних в бд
        # потрібно помістити зібрані дані в тимчасове сховище
        # якщо користувач надасть коректний ключ то дані будуть
        # вставлені в бд, а тимчасове сховище очищене
        df_temp = read_csv('static/csv/temp.csv')
        df_temp.loc[len(df_temp)] = row
        df_temp.to_csv('static/csv/temp.csv', index=False)

        # після цього переводимо користувача на сторінку підтвердження
        return redirect(url_for('apiget', action="secret-key"), code=307)
    else:
        return render_template("404.html")


@app.route('/secret-key-check', methods=['GET', 'POST'])
def secret_key():

    if request.method == 'POST':
        # беремо дані з реквесту
        req_data = request.get_json(force=True)
        # дістаємо секретний ключ
        key = req_data["Secret"]
        # підключаємося до тимчасових даних
        df_temp = read_csv('static/csv/temp.csv')

        # якщо ключ присутній в датафреймі, то робимо вставку в бд
        if key in df_temp.secret_key.values:
            # беремо індекс ключа
            key_idx = df_temp[df_temp.secret_key == key].index[0]
            # дістаємо всі дані, окрім ключа за індексом
            data = df_temp.iloc[key_idx, :14].to_dict()

            # ініціалізуємо об'єкти класів які являють собою проекції таблиць в бд
            client_acc_log = ClientAccLog()
            user_logins = UserLogins()
            client = Client()

            # тепер виконуємо операції вставки
            client_acc_log.insert(
                id=data['iban'],
                status='active'
            )

            user_logins.insert(
                login=data['email'],
                password=data['password'],
                question=data['question'],
                answer=data['answer'],
                acc_id=data['iban']
            )

            client.insert(
                acc_id=data['iban'],
                name=data['name'],
                surname=data['surname'],
                city=data['city'],
                region=data['region'],
                pass_type=data['pass_type'],
                pass_id=str(data['pass_id']) if data['se_pass'] is None else str(data['se_pass']) + str(data['pass_id']),
                ipn=str(data['ipn']),
                phone='+' + str(data['phone'])
            )

            # так як тепер користувач зареєстрований можна його
            # видалити з тимчасового кешу
            df_temp = df_temp.drop(key_idx)
            df_temp.to_csv('static/csv/temp.csv', index=False)
            # відправляємо запит на сторону клієнта про вдале підтвердження
            # статус 200 означає, що все пройшло успішно
            return make_response(jsonify({'redirect': '/bank/secret-key-approved'}), 200)

        # якщо ключа немає то надсилаємо на сторону клієнта помилку
        else:
            answer = {'Bad key': 'Key is not valid'}
            # відповідь з кодом 500 означає помилку сервера
            resp = make_response(jsonify(answer), 500)
            return resp

    else:
        # якщо сталась помилка
        return render_template("404.html")


if __name__ == "__main__":
    # df_temp = read_csv('static/csv/temp.csv')
    # idx = df_temp[df_temp.secret_key == 'pIMTt8gLjbWUaGwDtcwARUQJDrM4JrfydKBYvbfmvdMmVqLKnKILLgbC4nXLbR42'].index[0]
    # df_temp = df_temp.drop(idx)
    # print(df_temp)
    # df_temp.to_csv('static/csv/temp.csv', index=False)
    # columns = ['name', 'surname', 'email', 'pass_type', 'se_pass', 'pass_id', 'ipn',
    #            'region', 'city', 'phone', 'password', 'question', 'answer', 'iban',
    #            'secret_key']
    # df_temp = DataFrame(columns=columns)
    # df_temp.reset_index(drop=True)
    # df_temp.drop(df_temp.index, inplace=True)
    # print(df_temp)
    # print(df_temp.secret_key.values)
    # print(df_temp.iloc[idx, :14].to_dict())
    app.run(debug=True)

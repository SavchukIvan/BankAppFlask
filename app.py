from flask import Flask, session, g, render_template, request, redirect, url_for, make_response, jsonify, flash
from pandas import read_csv, DataFrame
from flask_mail import Mail, Message
from dao.table_methods import *
from helpers.datagen import *
from helpers.user import *
from helpers.card import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ewhvfgegyVYAQGYVBehg82t7y3882yeuhhddh2yu87u9y8U9YYTu9Y8U98YY8UhUVAGuvhqv'
app.config.from_pyfile('helpers/config.cfg')
mail = Mail(app)

global icard
icard = None
generator = Luhn()
client_acc_log = ClientAccLog()
userlogin = UserLogins()
client = Client()


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


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        result = userlogin.get_by_id(id=session['user_id'])
        user = result.first()
        user = User(id=user[0], email=user[1], password=user[2], logid=user[-1])
        g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        email = request.form['email']
        password = request.form['password']

        userlogin = UserLogins()
        result = userlogin.get_by_email(email=email)
        user = result.first()

        if user is None:
            flash('Ви ввели некоректні дані')
            return redirect(url_for('login'))

        if password == user[2]:
            session['user_id'] = user[0]
            return redirect(url_for('profile'))

        flash('Ви ввели некоректні дані')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if g.user:
        return render_template('user_page.html')

    return redirect(url_for('login'))


@app.route('/card', methods=['GET', 'POST'])
def card():
    global icard
    icard = None
    if g.user:
        card_inf = generator.create_card()
        card = Cards(num=card_inf['number'],
                     pin=card_inf['pin'],
                     cvv=card_inf['cvv'],
                     start=card_inf['start'],
                     end=card_inf['end'])
        icard = card

        cardinfo = CardInfo()
        info = cardinfo.get_all()
        tariffs = []

        for i in info:
            tariffs.append(i[0])

        st = card_inf['number']
        num = st[:4] + ' ' + st[4:8] + ' ' + st[8:12] + ' ' + st[12:16]
        return render_template('card_creation.html',
                               card=card,
                               num=num,
                               date=str(card_inf['start'].date())[-5:],
                               tariffs=tariffs)

    return redirect(url_for('login'))


@app.route('/card-create', methods=['GET', 'POST'])
def card_creation():
    if g.user:
        if icard:
            if request.method == 'POST':
                data = request.form

                tariff = data['tariff']
                ctype = data['ctype']

                dbcard = Card()
                cardinfo = CardInfo()

                result = cardinfo.get_by_tariff(tariff=tariff)
                ci = result.first()

                dbcard.insert(
                    id=icard.num,
                    pin=icard.pin,
                    cvv=icard.cvv,
                    type=ctype,
                    tariff=tariff,
                    status='active',
                    rdate=icard.start,
                    vdate=icard.end,
                    money=0,
                    limit=ci[-1],
                    bonuses=0,
                    acc_id=g.user.logid
                )

                return redirect(url_for('profile'))

        else:
            return render_template("404.html")

    return redirect(url_for('login'))


@app.route('/bank/<action>', methods=['GET', 'POST'])
def apiget(action):
    '''
        Функція, що оперує роутами програми
        без зареєстрованого користувача,
        кожний роут переводить користувача
        на відповідну сторінку, також
        присутня сторінка з помилкою
    '''
    if g.user:
        return redirect(url_for('profile'))

    if action == 'reg':
        return render_template('reg_page.html')

    elif action == "secret-key":
        return render_template("secret_key.html")

    elif action == "secret-key-approved":
        return render_template("secret_key_approved.html")

    else:
        return render_template("404.html")


@app.route('/', methods=['GET', 'POST'])
def main_index():
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
    if g.user:
        render_template("404.html")

    if request.method == 'POST':
        # отримуємо дані з форми
        reg = request.form
        # зберігаємо дані до списку
        row = [str(i) for i in reg.to_dict().values()]
        # якщо тип "картка", то серія паспорту не повертається
        # доводиться вставляти власноруч
        if row[3] == 'card':
            row.insert(4, 'NO')
        # перед тим як продовжувати роботу програми
        # варто перевірити чи вже немає таких даних

        result = userlogin.get_by_email(email=row[2])
        email = result.first()
        if email is not None:
            return make_response(jsonify({'Email': 'Is not valid'}), 500)

        result = client.get_by_passid(pass_id=row[4]+row[5])
        ps = result.first()
        if ps is not None:
            return make_response(jsonify({'PassportID': 'Is not valid'}), 500)

        result = client.get_by_phone(phone=row[9])
        ph = result.first()
        if ph is not None:
            return make_response(jsonify({'Phone': 'Is not valid'}), 500)

        result = client.get_by_ipn(ipn=row[6])
        ipn = result.first()
        if ipn is not None:
            return make_response(jsonify({'IPN': 'Is not valid'}), 500)

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
        return make_response(jsonify({'redirect': '/bank/secret-key'}), 200)
    else:
        return render_template("404.html")


@app.route('/secret-key-check', methods=['GET', 'POST'])
def secret_key():
    if g.user:
        render_template("404.html")

    if request.method == 'POST':
        # беремо дані з реквесту
        req_data = request.form
        # дістаємо секретний ключ
        key = req_data["key"]
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
                pass_id=str(data['pass_id']) if data['se_pass'] == 'NO' else str(data['se_pass']) + str(data['pass_id']),
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

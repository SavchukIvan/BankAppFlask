from flask import Flask, session, g, render_template, request, redirect, url_for, make_response, jsonify, flash
from flask_mail import Mail, Message
from dao.table_methods import *
from datetime import timedelta
from helpers.datagen import *
from helpers.tmpcl import *
from helpers.user import *
from helpers.card import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ewhvfgegyVYAQGYVBehg82t7y3882yeuhhddh2yu87u9y8U9YYTu9Y8U9fbeuhf87d7v88dcJBJNd8fy78d8d7v8d8v8dyv8XGTCDESD7dfv9cyduv8yvuyJBGVLLNUdfy8ydvy8dy7v8dyfer83u83u8y83u8fyu8yuuvghufgynbhbvdhxbjhwgeujb3bBFXY75FTR3Q3EYVbjbhb3j2bhbj2bh32bj3bhb3j2bv3bkbv21nkb3hnkrb3bj3bvy3vh4bhhfcg3bgcJNBJ4b2cdeug8YY8UhUVAGu233vhqv'
app.config.from_pyfile('helpers/config.cfg')
mail = Mail(app)

global icard
icard = None
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


@app.before_request
def before_request():
    '''
        Перед кожним переходом на іншу сторінку
        нам потрібно переконатися, що юзер знаходиться в системі
    '''
    g.user = None

    if 'user_id' in session:
        # це здається має зробити час сессії 5 хв
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)

        # надаємо глобальній змінній юзера параметри які ми надалі
        # можемо використовувати в програмі
        userlogin = UserLogins()
        result = userlogin.get_by_id(id=session['user_id'])
        user = result.first()
        user = User(id=user[0], email=user[1], password=user[2], logid=user[-1])
        g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():

    # дістаємо дані логіна на паролю з форми
    if request.method == 'POST':
        session.pop('user_id', None)
        email = request.form['email']
        password = request.form['password']

        # дивимося чи є такі дані в бд
        userlogin = UserLogins()
        result = userlogin.get_by_email(email=email)
        user = result.first()

        if user is None:
            flash('Ви ввели некоректні дані')
            return redirect(url_for('login'))

        # якщо юзер є то перевіряємо пароль
        if password == user[2]:
            # створюємо сесію по id користувача
            session['user_id'] = user[0]
            # переводимо людину в профіль
            return redirect(url_for('profile', action='cards'))

        flash('Ви ввели некоректні дані')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/profile/<action>', methods=['GET', 'POST'])
def profile(action):
    # якщо юзер в системі...
    if g.user:
        # дістаємо всі його картки
        crd = Card()
        result = crd.get_by_accid(accid=g.user.logid)
        result = list(result)
        ncards = len(result)
        cardsnum = [i+1 for i in range(ncards)]

        # якщо карток 4 то не показуємо кнопку створення картки
        show = True
        if ncards == 4:
            show = False

        # показуємо сторінку без рендерених карток
        if action == 'cards':

            if len(result) == 0:
                # сторінка взагалі без карток
                return render_template('user_page.html', exist=False,
                                       render=False, showbut=show)
            else:
                # сторінка на якій є картки
                return render_template('user_page.html', exist=True,
                                       render=False, showbut=show,
                                       cardsnum=cardsnum)

        # перевіряємо роут користувача
        actions = ['card1', 'card2', 'card3', 'card4']
        if action in actions:

            if int(action[-1]) > ncards:
                return render_template("404.html")
            else:
                # дістаємо та розподіляємо всі дані по картці
                crd = result[int(action[-1]) - 1]  # дістаємо потрібну картку
                num = crd[0][:4] + ' ' + crd[0][4:8] + ' ' + crd[0][8:12] + ' ' + crd[0][12:16]
                pin = crd[1]
                cvv = crd[2]
                tariff = crd[4]
                date = str(crd[7].date())[-5:]
                money = crd[8]
                bonuses = crd[10]
                limit = crd[9]

                # передаємо всі дані на сторінку, та рендеримо картку
                return render_template('user_page.html',
                                       exist=True,
                                       render=True,
                                       showbut=show,
                                       cardsnum=cardsnum,
                                       idx=int(action[-1]),
                                       money=money,
                                       bonuses=bonuses,
                                       limit=limit,
                                       num=num,
                                       tariff=tariff,
                                       date=date,
                                       cvv=cvv)

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    '''
        Якщо юзер бажає покинути профіль,
        то просто виймаємо його id з сесії
    '''
    session.pop('user_id', None)

    return redirect(url_for('login'))


@app.route('/card', methods=['GET', 'POST'])
def card():

    global icard
    icard = None

    if g.user:
        # дивимося чи немає в юзера 4 картки
        crd = Card()
        result = crd.get_by_accid(accid=g.user.logid)
        result = list(result)
        ncards = len(result)

        # якщо картки 4, то ця сторінка йому не доступна
        if ncards == 4:
            return render_template("404.html")

        # звертаємося до функції в helpers, та генеруємо всі дані картки
        card_inf = generator.create_card()
        # тимчасово зберіємо їх в спеціальному класі
        card = Cards(num=card_inf['number'],
                     pin=card_inf['pin'],
                     cvv=card_inf['cvv'],
                     start=card_inf['start'],
                     end=card_inf['end'])
        icard = card

        # дістаємо всі тарифи, що є
        cardinfo = CardInfo()
        info = cardinfo.get_all()
        tariffs = []

        for i in info:
            tariffs.append(i[0])

        # дістаємо всі картки, що є
        cardtype = CardTypeInfo()
        info = cardtype.get_all()
        types = []

        for i in info:
            types.append(i[0])

        existing = []
        for i in result:
            existing.append(i[3])

        if 'Credit' in existing:
            types.remove('Credit')

        st = card_inf['number']
        # це для того, щоб гарно відмалювати картку
        num = st[:4] + ' ' + st[4:8] + ' ' + st[8:12] + ' ' + st[12:16]
        # передаємо всі дані на сторінку
        return render_template('card_creation.html',
                               card=card,
                               num=num,
                               date=str(card_inf['start'].date())[-5:],
                               tariffs=tariffs,
                               types=types)

    return redirect(url_for('login'))


@app.route('/card-create', methods=['GET', 'POST'])
def card_creation():

    # якщо юзер в сесії...
    if g.user:
        # якщо створений екземпляр класу icard(глобальна змінна)
        if icard:
            # збираємо всі дані з форми
            if request.method == 'POST':
                data = request.form

                tariff = data['tariff']
                ctype = data['ctype']

                # ініціалізуємо з'єднання з бд
                dbcard = Card()
                cardinfo = CardInfo()
                cardtype = CardTypeInfo()

                # дістаємо інформацію про тарифи
                result = cardtype.get_by_type(cardtype=ctype)
                ci = result.first()

                # вставляємо карту в бд
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

                return redirect(url_for('profile', action='cards'))

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
        global tmp
        tmp = TMPClient(
            name=reg["name"],
            surname=reg["surname"],
            email=reg["email"],
            pass_type=reg["passport_type"],
            pass_id=reg["pass_id"],
            ipn=reg["IPN"],
            region=reg["region"],
            city=reg["city"],
            phone=reg["phone_numb"],
            password=reg["password"],
            question=reg["secret"],
            answer=reg["answer"],
            se_pass='' if reg["passport_type"] == 'card' else reg["se_pass"],
            iban=generator.create_(),
            secret_key=get_random_alphanumeric_string(64)
        )

        # перед тим як продовжувати роботу програми
        # варто перевірити чи вже немає таких даних

        userlogin = UserLogins()
        result = userlogin.get_by_email(email=tmp.email)
        email = result.first()
        if email is not None:
            return make_response(jsonify({'Email': 'Is not valid'}), 500)

        client = Client()
        result = client.get_by_passid(pass_id=tmp.se_pass+tmp.pass_id)
        ps = result.first()
        if ps is not None:
            return make_response(jsonify({'PassportID': 'Is not valid'}), 500)

        result = client.get_by_phone(phone=tmp.phone)
        ph = result.first()
        if ph is not None:
            return make_response(jsonify({'Phone': 'Is not valid'}), 500)

        result = client.get_by_ipn(ipn=tmp.ipn)
        ipn = result.first()
        if ipn is not None:
            return make_response(jsonify({'IPN': 'Is not valid'}), 500)

        # надсилаємо секретний ключ на пошту користувачу
        send_email(email=tmp.email, code=tmp.secret_key)

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

        # якщо ключ присутній в датафреймі, то робимо вставку в бд
        if key == tmp.secret_key:

            # ініціалізуємо об'єкти класів які являють
            #  собою проекції таблиць в бд
            client_acc_log = ClientAccLog()
            user_logins = UserLogins()
            client = Client()

            # тепер виконуємо операції вставки
            client_acc_log.insert(
                id=tmp.iban,
                status='active'
            )

            user_logins.insert(
                login=tmp.email,
                password=tmp.password,
                question=tmp.question,
                answer=tmp.answer,
                acc_id=tmp.iban
            )

            client.insert(
                acc_id=tmp.iban,
                name=tmp.name,
                surname=tmp.surname,
                city=tmp.city,
                region=tmp.region,
                pass_type=tmp.pass_type,
                pass_id=tmp.se_pass + tmp.pass_id,
                ipn=tmp.ipn,
                phone=tmp.phone
            )

            # відправляємо запит на сторону клієнта про вдале підтвердження
            # статус 200 означає, що все пройшло успішно
            resp = {'redirect': '/bank/secret-key-approved'}
            return make_response(jsonify(resp), 200)

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
    app.run(debug=True)

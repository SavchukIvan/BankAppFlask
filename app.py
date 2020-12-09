from flask import Flask, session, g, render_template, request, redirect, url_for, make_response, jsonify, flash, json
from flask_mail import Mail, Message
from sqlalchemy import MetaData
from dao.PostgresDB import *
from dao.table_methods import *
import datetime
from datetime import timedelta
from datetime import datetime
from helpers.datagen import *
from helpers.tmpcl import *
from helpers.user import *
from helpers.card import *
from helpers.plots import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ewhvfgegyVYAQGYVBehg82t7y3882yeuhhddh2yu87u9y8U9YYTu9Y8U9fbeuhf87d7v88dcJBJNd8fy78d8d7v8d8v8dyv8XGTCDESD7dfv9cyduv8yvuyJBGVLLNUdfy8ydvy8dy7v8dyfer83u83u8y83u8fyu8yuuvghufgynbhbvdhxbjhwgeujb3bBFXY75FTR3Q3EYVbjbhb3j2bhbj2bh32bj3bhb3j2bv3bkbv21nkb3hnkrb3bj3bvy3vh4bhhfcg3bgcJNBJ4b2cdeug8YY8UhUVAGu233vhqv'
app.config.from_pyfile('helpers/config.cfg')
mail = Mail(app)

generator = Luhn()

db = PostgresDb()
sessio = db.sqlalchemy_session
metadata = MetaData(bind=db.sqlalchemy_engine)

client_acc_log = ClientAccLog(session=sessio, meta=metadata)
user_logins = UserLogins(session=sessio, meta=metadata)
client = Client(session=sessio, meta=metadata)
ucard = Card(session=sessio, meta=metadata)
cardinfo = CardInfo(session=sessio, meta=metadata)
cardtype = CardTypeInfo(session=sessio, meta=metadata)
transinfo = TransInfo(session=sessio, meta=metadata)
transact = Transaction(session=sessio, meta=metadata)
tmp_crd = TMPCard(session=sessio, meta=metadata)
tmp_cli = TMPClientInf(session=sessio, meta=metadata)


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
    g.admin = None

    if 'user_id' in session:
        # це здається має зробити час сессії 5 хв
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)

        # надаємо глобальній змінній юзера параметри які ми надалі
        # можемо використовувати в програмі
        result = user_logins.get_by_id(id=session['user_id'])
        user = result.first()
        res = client_acc_log.get_by_id(id=user[-1])
        acc_status = res.first()
        user = User(id=user[0],
                    email=user[1],
                    password=user[2],
                    logid=user[-1],
                    status=acc_status[1])
        g.user = user

    if 'admin' in session:
        # це здається має зробити час сессії 5 хв
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)

        # надаємо глобальній змінній юзера параметри які ми надалі
        # можемо використовувати в програмі
        result = user_logins.get_by_id(id=session['admin'])
        user = result.first()
        res = client_acc_log.get_by_id(id=user[-1])
        acc_status = res.first()
        user = User(id=user[0],
                    email=user[1],
                    password=user[2],
                    logid=user[-1],
                    status=acc_status[1])
        g.admin = admin


@app.route('/login', methods=['GET', 'POST'])
def login():

    # дістаємо дані логіна на паролю з форми
    if request.method == 'POST':
        session.pop('user_id', None)
        email = request.form['email']
        password = request.form['password']

        # дивимося чи є такі дані в бд
        result = user_logins.get_by_email(email=email)
        user = result.first()

        if user is None:
            flash('Ви ввели некоректні дані')
            return redirect(url_for('login'))

        res = client_acc_log.get_by_id(id=user[-1])
        acc_status = res.first()[1]

        # якщо юзер є то перевіряємо пароль
        if acc_status == 'active' and password == user[2]:
            # створюємо сесію по id користувача
            session['user_id'] = user[0]
            # переводимо людину в профіль
            return redirect(url_for('profile', action='cards'))

        elif acc_status == 'admin' and password == user[2]:
            # створюємо сесію по id користувача
            session['admin'] = user[0]
            # переводимо людину в профіль
            return redirect(url_for('admin'))

        elif acc_status == 'blocked' and password == user[2]:
            flash('Ваш профіль був заблокований адміністрацією')
            return redirect(url_for('login'))

        flash('Ви ввели некоректні дані')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    '''
        Якщо юзер бажає покинути профіль,
        то просто виймаємо його id з сесії
    '''
    session.pop('user_id', None)

    return redirect(url_for('login'))


@app.route('/logout_admin')
def logout_admin():
    '''
        Якщо юзер бажає покинути профіль,
        то просто виймаємо його id з сесії
    '''
    session.pop('admin', None)

    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if g.admin:

        cdif = cardinfo.get_all()
        tariffs = []
        bonuscoefs = []
        for row in cdif:
            tariffs.append(row[0])
            bonuscoefs.append(row[1])

        num1 = [i+1 for i in range(len(tariffs))]

        cdt = cardtype.get_all()
        types = []
        limits = []
        for row in cdt:
            types.append(row[0])
            limits.append(row[1])

        num2 = [i+1 for i in range(len(types))]

        cursor = db.execute('''
                            SELECT CardType, COUNT(CardType) Number_of_cards
                            FROM Card
                            GROUP BY CardType;
                            '''
                            )
        labels = []
        values = []
        for row in cursor:
            labels.append(row[0])
            values.append(row[1])

        pie_type = pie_plot(labels=labels,
                            values=values,
                            title='Відношення типів карток в системі')

        cursor = db.execute('''
                            SELECT Tariff, COUNT(Tariff) Number_of_cards
                            FROM Card
                            GROUP BY Tariff;
                            '''
                            )
        labels = []
        values = []
        for row in cursor:
            labels.append(row[0])
            values.append(row[1])

        pie_tariff = pie_plot(labels=labels,
                              values=values,
                              title='Відношення тарифів карток в системі')

        activityBar = plot_activity(db=db)
        return render_template('admin.html',
                               cardinfo=zip(num1, tariffs, bonuscoefs),
                               cardtype=zip(num2, types, limits),
                               pie_type=pie_type,
                               pie_tariff=pie_tariff,
                               activityBar=activityBar)

    return render_template('login.html')


@app.route('/user_ban_unban', methods=['GET', 'POST'])
def user_ban_unban():

    if g.admin:

        return render_template('user_ban_unban.html')

    return render_template('login.html')


@app.route('/update_user_status', methods=['GET', 'POST'])
def update_user_status():

    if g.admin:
        if request.method == 'POST':
            data = request.form

            result = user_logins.get_by_email(email=data['email'])
            user = result.first()

            if user is None:
                flash('Користувача з таким емейлом не існує', 'danger')
                return redirect(url_for('user_ban_unban'))

            client_acc_log.update(
                id=user[-1],
                status=data["status"]
            )

            flash(f'Cтатус користувача з логіном {data["email"]} змінено на {data["status"]}', 'success')
            return render_template('user_ban_unban.html')

    return render_template('login.html')


@app.route('/card_ban_unban', methods=['GET', 'POST'])
def card_ban_unban():

    if g.admin:

        return render_template('card_ban_unban.html')

    return render_template('login.html')


@app.route('/update_card_status', methods=['GET', 'POST'])
def update_card_status():

    if g.admin:
        if request.method == 'POST':
            data = request.form

            result = ucard.get_by_cardid(data["card"].replace(" ", ""))
            cardd = result.first()

            if cardd is None:
                flash('Картки з таким номером не існує', 'danger')
                return redirect(url_for('user_ban_unban'))

            ucard.update_card_status(
                id=data["card"].replace(" ", ""),
                status=data["status"]
            )

            flash(f'Статус картки з номером {data["card"].replace(" ", "")} змінено на {data["status"]}', 'success')
            return render_template('card_ban_unban.html')

    return render_template('login.html')


@app.route('/update_tariff', methods=['GET', 'POST'])
def update_tariff():

    if g.admin:
        data = request.form

        cardinfo.update(
            tariff=data["tariff"],
            bonus_coef=float(data["bonus"].replace(',', '.'))
        )

        return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/update_type', methods=['GET', 'POST'])
def update_type():

    if g.admin:
        data = request.form

        cardtype.update(
            cardtype=data["type"],
            credit_limit=float(data["limit"].replace(',', '.'))
        )

        return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/transaction', methods=['GET', 'POST'])
def transaction():

    if g.user:

        result = ucard.get_by_accid(accid=g.user.logid)
        result = list(result)
        numbers = [str(result[i][0]) for i in range(len(result))]
        moneys = [str(result[i][8]) for i in range(len(result))]
        type = [result[i][3] for i in range(len(result))]

        return render_template('transaction.html',
                               card_money=zip(numbers, moneys, type))

    return render_template('login.html')


@app.route('/transact_submit', methods=['GET', 'POST'])
def transact_submit():

    if g.user:
        if request.method == 'POST':

            result = transinfo.get_by_trans_type(trans_type='transfer')
            com_coef = result.first()[0]

            data = request.form
            sender_card = data["senderCard"][:16]
            receiver_card = data["receiverCard"].replace(" ", "")
            sum = float(data["sum"])
            commission = com_coef*sum
            total_sum = sum + commission

            result = ucard.get_bonuscoef_by_id(sender_card, cardinfo)
            bon_coef = result.first()[-1]

            bonuses_received = sum*bon_coef

            result = ucard.get_by_cardid(cardid=receiver_card)
            receiver_exist = result.first()

            if receiver_exist is None:
                return make_response(jsonify({'Card': 'Receiver card is not exist'}), 500)

            result = ucard.get_name_surname_by_cardid(receiver_card,
                                                      client_acc_log,
                                                      client)
            row = result.first()[-2:]
            receiver_name = row[0] + " " + row[1]

            result = ucard.get_money_by_cardid(cardid=sender_card)
            money_in_card = result.first()[0]

            result = ucard.get_limit_by_cardid(cardid=sender_card)
            limit_in_card = result.first()[0]

            if (money_in_card - total_sum) < -limit_in_card:
                return make_response(jsonify({'Money': 'Limit is overdrafted'}), 500)

            resp = {"sender_card": sender_card,
                    "receiver_card": receiver_card,
                    "sum": sum,
                    "purpose": data["purpose"],
                    "commission": commission,
                    "total_sum": total_sum,
                    "bonuses_received": bonuses_received,
                    "receiver_name": receiver_name}

            session["messages"] = json.dumps(resp)
            return make_response(jsonify({'Message': 'It`s okay there!'}), 200)
        else:
            redirect(url_for('profile', action='cards'), code=301)

    return render_template('login.html')


@app.route('/transact_approve', methods=['GET', 'POST'])
def transact_approve():

    if g.user:
        data = session["messages"]
        session.pop("messages", None)

        return render_template('transact_submit.html', data=json.loads(data))

    return render_template('login.html')


@app.route('/transact_execute', methods=['GET', 'POST'])
def transact_execute():

    if g.user:
        if request.method == 'POST':
            data = request.form

            result = ucard.get_status_by_cardid(cardid=data["senderCard"])
            status = result.first()[-1]

            if status == 'blocked':
                flash('Картка з якої здійснювалась транзакція наразі заблокована')
                return redirect(url_for('profile', action='cards'))

            transact.insert(
                cardid=data["senderCard"],
                rcardid=data["receiverCard"],
                inisum=data["sum"],
                comsum=data["commission"],
                totsum=data["totalSum"],
                bonusesrec=data["bonuses"],
                transtime=datetime.datetime.now(),
                transdesc=data["purpose"],
                transtype="transfer"
            )

            return render_template('transact_success.html')
        else:
            return redirect(url_for('profile', action='cards'), code=301)

    return render_template('login.html')


@app.route('/profile/<action>', methods=['GET', 'POST'])
def profile(action):
    # якщо юзер в системі...
    if g.user:
        # дістаємо всі його картки
        result = ucard.get_by_accid(accid=g.user.logid)
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
                values = []
                labels = []
                title = 'Баланс на ваших картках'
                k = 1
                for i in result:
                    values.append(i[8])
                    labels.append(f'card{k}')
                    k += 1

                balance_on_cards = barchart_cards(labels=labels,
                                                  values=values,
                                                  title=title)

                trendBoard = plot_season_stl(db, g.user.logid)
                # сторінка на якій є картки
                return render_template('user_page.html',
                                       exist=True,
                                       render=False,
                                       showbut=show,
                                       cardsnum=cardsnum,
                                       balance_on_cards=balance_on_cards,
                                       trendBoard=trendBoard)

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
                status = crd[5]
                date = str(crd[7].date())[2:7]
                money = crd[8]
                bonuses = crd[10]
                limit = crd[9]

                bonusesShow = False
                if bonuses >= 100:
                    bonusesShow = True

                linearModel = plot_linear_regression(db=db,
                                                     accountid=g.user.logid,
                                                     cardid=crd[0])
                # передаємо всі дані на сторінку, та рендеримо картку
                return render_template('user_page.html',
                                       exist=True,
                                       render=True,
                                       showbut=show,
                                       cardsnum=cardsnum,
                                       idx=int(action[-1]),
                                       money=money,
                                       status=status,
                                       bonuses=bonuses,
                                       limit=limit,
                                       num=num,
                                       tariff=tariff,
                                       date=date,
                                       cvv=cvv,
                                       linearModel=linearModel,
                                       bonusesShow=bonusesShow)

    return render_template('login.html')


@app.route('/getbonuses/<cardnum>', methods=['GET', 'POST'])
def getbonuses(cardnum):
    if g.user:
        result = ucard.get_by_accid(accid=g.user.logid)
        result = list(result)
        crd = result[int(cardnum[-1]) - 1]
        money = crd[8]
        bonuses = crd[10]
        num = crd[0]

        status = crd[5]

        if status == 'blocked':
            flash(f'Картку {num} наразі заблоковано, зверніться до адміністрації')
            return redirect(url_for('profile', action='cards'))

        db.execute(
        f'''
        UPDATE Card
        SET MONEYAMOUNT = {money + bonuses*2}
        WHERE CARDID = '{num}'
        '''
        )
        db.execute(
        f'''
        UPDATE Card
        SET BONUSES = 0
        WHERE CARDID = '{num}'
        '''
        )

        flash(f'Бонуси успішно зняті на картку {num}')
        return redirect(url_for('profile', action='cards'))

    return render_template('404.html')


@app.route('/card', methods=['GET', 'POST'])
def card():

    if g.user:
        # дивимося чи немає в юзера 4 картки
        result = ucard.get_by_accid(accid=g.user.logid)
        result = list(result)
        ncards = len(result)

        # якщо картки 4, то ця сторінка йому не доступна
        if ncards == 4:
            return redirect(url_for('profile', action='cards'))

        tmp_crd.delete(accid=g.user.logid)

        # звертаємося до функції в helpers, та генеруємо всі дані картки
        card_inf = generator.create_card()
        result1 = ucard.get_by_cardid(cardid=card_inf['number'])
        if result1 is not None:
            card_inf = generator.create_card()

        # тимчасово зберіємо їх в спеціальному класі
        icard = Cards(num=card_inf['number'],
                      pin=card_inf['pin'],
                      cvv=card_inf['cvv'],
                      start=card_inf['start'],
                      end=card_inf['end'])

        tmp_crd.insert(id=icard.num,
                       pin=icard.pin,
                       cvv=icard.cvv,
                       rdate=icard.start,
                       vdate=icard.end,
                       acc_id=g.user.logid)

        # дістаємо всі тарифи, що є
        info = cardinfo.get_all()
        tariffs = []

        for i in info:
            tariffs.append(i[0])

        # дістаємо всі картки, що є
        info = cardtype.get_all()
        types = []

        for i in info:
            types.append(i[0])

        existing = []
        for i in result:
            existing.append(i[3])

        if 'Credit' in existing:
            types.remove('Credit')

        debit_count = existing.count('Debit')
        if debit_count == 3:
            types.remove('Debit')

        st = card_inf['number']
        # це для того, щоб гарно відмалювати картку
        num = st[:4] + ' ' + st[4:8] + ' ' + st[8:12] + ' ' + st[12:16]
        # передаємо всі дані на сторінку
        return render_template('card_creation.html',
                               card=icard,
                               num=num,
                               date=str(card_inf['end'].date())[2:7],
                               tariffs=tariffs,
                               types=types)

    return render_template('login.html')


@app.route('/card-create', methods=['GET', 'POST'])
def card_creation():

    # якщо юзер в сесії...
    if g.user:
        # збираємо всі дані з форми
        if request.method == 'POST':
            data = request.form

            tariff = data['tariff']
            ctype = data['ctype']

            result = tmp_crd.get_by_accid(accid=g.user.logid)
            icard = result.first()
            # дістаємо інформацію про тарифи
            result = cardtype.get_by_type(cardtype=ctype)
            ci = result.first()

            # вставляємо карту в бд
            ucard.insert(
                id=icard[0],
                pin=icard[1],
                cvv=icard[2],
                type=ctype,
                tariff=tariff,
                status='active',
                rdate=icard[3],
                vdate=icard[4],
                money=0,
                limit=ci[-1],
                bonuses=0,
                acc_id=icard[5]
            )

            tmp_crd.delete(accid=icard[5])

            return redirect(url_for('profile', action='cards'), code=301)

        else:
            return redirect(url_for('profile', action='cards'), code=301)

    return render_template('login.html')


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
        return render_template("404.html")

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
        render_template('login.html')

    if request.method == 'POST':
        # отримуємо дані з форми
        reg = request.form
        # зберігаємо дані до списку

        se_pass = '' if reg["passport_type"] == 'card' else reg["se_pass"]
        pass_id = reg["pass_id"]
        # перед тим як продовжувати роботу програми
        # варто перевірити чи вже немає таких даних

        result = user_logins.get_by_email(email=reg["email"])
        email = result.first()
        if email is not None:
            return make_response(jsonify({'Email': 'Is not valid'}), 500)

        result = client.get_by_passid(pass_id=se_pass+pass_id)
        ps = result.first()
        if ps is not None:
            return make_response(jsonify({'PassportID': 'Is not valid'}), 500)

        result = client.get_by_phone(phone=('+380' + reg["phone_numb"]))
        ph = result.first()
        if ph is not None:
            return make_response(jsonify({'Phone': 'Is not valid'}), 500)

        result = client.get_by_ipn(ipn=reg["IPN"])
        ipn = result.first()
        if ipn is not None:
            return make_response(jsonify({'IPN': 'Is not valid'}), 500)

        # надсилаємо секретний ключ на пошту користувачу
        secret_key = get_random_alphanumeric_string(64)
        send_email(email=reg["email"], code=secret_key)

        tmp_cli.insert(
            name=reg["name"],
            surname=reg["surname"],
            email=reg["email"],
            pass_type=reg["passport_type"],
            se_pass='' if reg["passport_type"] == 'card' else reg["se_pass"],
            pass_id=reg["pass_id"],
            ipn=reg["IPN"],
            region=reg["region"],
            city=reg["city"],
            phone=('+380'+reg["phone_numb"]),
            password=reg["password"],
            question=reg["secret"],
            answer=reg["answer"],
            iban=generator.create_(),
            secret=secret_key
        )
        # після цього переводимо користувача на сторінку підтвердження
        return make_response(jsonify({'redirect': '/bank/secret-key'}), 200)
    else:
        return render_template("404.html")


@app.route('/secret-key-check', methods=['GET', 'POST'])
def secret_key():

    if g.user:
        render_template('login.html')

    if request.method == 'POST':
        # беремо дані з реквесту
        req_data = request.form
        # дістаємо секретний ключ
        key = req_data["key"]

        result = tmp_cli.get_by_secret(secret=key)
        tmp = result.first()

        if key == tmp[-1]:

            # ініціалізуємо об'єкти класів які являють
            #  собою проекції таблиць в бд

            # тепер виконуємо операції вставки
            client_acc_log.insert(
                id=tmp[-2],
                status='active'
            )

            user_logins.insert(
                login=tmp[2],
                password=tmp[-5],
                question=tmp[-4],
                answer=tmp[-3],
                acc_id=tmp[-2]
            )

            client.insert(
                acc_id=tmp[-2],
                name=tmp[0],
                surname=tmp[1],
                city=tmp[8],
                region=tmp[7],
                pass_type=tmp[3],
                pass_id=tmp[4] + tmp[5],
                ipn=tmp[6],
                phone=tmp[9]
            )
            tmp_cli.delete(secret=key)
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

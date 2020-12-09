from sqlalchemy import Table, MetaData, Column, VARCHAR, Float, DateTime, Integer, ForeignKey
from dao.PostgresDB import *
# from PostgresDB import *
from sqlalchemy import desc


class ClientAccLog:
    '''
        Інформація та методи
        для таблиці ClientAccLog
    '''
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('clientacclog', self.metadata,
                           Column('accountid', VARCHAR(80), primary_key=True),
                           Column('accountstatus', VARCHAR(40), nullable=False),
                           autoload=True, extend_existing=True)

    def get_by_id(self, id):
        select_stmt = select([self.table]).\
                      where(self.table.c.accountid == id)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, id, status):

        query = self.table.insert().\
            values({'accountid': id,
                    'accountstatus': status})

        self.session.execute(query)
        self.session.commit()

    def delete(self, id):
        query = self.table.delete().\
            where(self.table.c.accountid == id)

        self.session.execute(query)
        self.session.commit()

    def update(self, id, status):
        query = self.table.update().\
            where(self.table.c.accountid == id).\
            values({'accountstatus': status})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class UserLogins:
    '''
        Інформація та методи
        для таблиці UserLogins
    '''
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('userlogins', self.metadata,
                           Column('userid', Integer, primary_key=True, autoincrement=True),
                           Column('userlogin', VARCHAR(40), primary_key=True),
                           Column('userpassword', VARCHAR(40), nullable=False),
                           Column('usersecurityanswer', VARCHAR(40), nullable=False),
                           Column('usersecurityquestion', VARCHAR(80), nullable=False),
                           Column('accountid', VARCHAR(40), ForeignKey('clientacclog.accountid')),
                           autoload=True, extend_existing=True)

    def get_by_email(self, email):
        select_stmt = select([self.table]).\
                      where(self.table.c.userlogin == email)
        result = self.session.execute(select_stmt)
        return result

    def get_by_id(self, id):
        select_stmt = select([self.table]).\
                      where(self.table.c.userid == id)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, login, password, question, answer, acc_id):

        query = self.table.insert().\
            values({'userlogin': login,
                    'userpassword': password,
                    'usersecurityanswer': answer,
                    'usersecurityquestion': question,
                    'accountid': acc_id})

        self.session.execute(query)
        self.session.commit()

    def delete(self, login):
        query = self.table.delete().\
            where(self.table.c.userlogin == login)

        self.session.execute(query)
        self.session.commit()

    def update(self, login, password, question, answer, acc_id):
        query = self.table.update().\
            where(self.table.c.userlogin == login).\
            values({'userpassword': password,
                    'usersecurityanswer': answer,
                    'usersecurityquestion': question,
                    'accountid': acc_id})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class Client:
    '''
        Інформація та методи
        для таблиці UserLogins
    '''
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('client', self.metadata,
                           Column('clientid', Integer, primary_key=True),
                           Column('accountid', VARCHAR(40), ForeignKey('clientacclog.accountid')),
                           Column('firstname', VARCHAR(40), nullable=False),
                           Column('lastname', VARCHAR(40), nullable=False),
                           Column('city', VARCHAR(40), nullable=False),
                           Column('region', VARCHAR(40)),
                           Column('passporttype', VARCHAR(40), nullable=False),
                           Column('passportid', VARCHAR(40), nullable=False, unique=True),
                           Column('ipn', VARCHAR(40), nullable=False, unique=True),
                           Column('phone', VARCHAR(40), nullable=False, unique=True),
                           autoload=True, extend_existing=True)

    def get_by_phone(self, phone):
        select_stmt = select([self.table]).\
                      where(self.table.c.phone == phone)
        result = self.session.execute(select_stmt)
        return result

    def get_by_ipn(self, ipn):
        select_stmt = select([self.table]).\
                      where(self.table.c.ipn == ipn)
        result = self.session.execute(select_stmt)
        return result

    def get_by_passid(self, pass_id):
        select_stmt = select([self.table]).\
                      where(self.table.c.passportid == pass_id)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, acc_id, name, surname,
               city, region, pass_type, pass_id, ipn, phone):

        query = self.table.insert().\
            values({'accountid': acc_id,
                    'firstname': name,
                    'lastname': surname,
                    'city': city,
                    'region': region,
                    'passporttype': pass_type,
                    'passportid': pass_id,
                    'ipn': ipn,
                    'phone': phone})

        self.session.execute(query)
        self.session.commit()

    def delete(self, acc_id):
        query = self.table.delete().\
            where(self.table.c.accountid == acc_id)

        self.session.execute(query)
        self.session.commit()

    def update(self, acc_id, name, surname, city,
               region, pass_type, pass_id, ipn, phone):

        query = self.table.update().\
            where(self.table.c.accountid == acc_id).\
            values({'firstname': name,
                    'lastname': surname,
                    'city': city,
                    'region': region,
                    'passporttype': pass_type,
                    'passportid': pass_id,
                    'ipn': ipn,
                    'phone': phone})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class CardInfo:
    '''
        Інформація та методи
        для таблиці CardInfo
    '''
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('cardinfo', self.metadata,
                           Column('tariff', VARCHAR(40), primary_key=True),
                           Column('bonuscoef', Float, nullable=False),
                           autoload=True, extend_existing=True)

    def get_all(self):
        result = self.session.query(self.table).all()
        return result

    def get_by_tariff(self, tariff):
        select_stmt = select([self.table]).\
                      where(self.table.c.tariff == tariff)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, tariff, bonus_coef):

        query = self.table.insert().\
            values({'tariff': tariff,
                    'bonuscoef': bonus_coef})

        self.session.execute(query)
        self.session.commit()

    def delete(self, tariff):
        query = self.table.delete().\
            where(self.table.c.tariff == tariff)

        self.session.execute(query)
        self.session.commit()

    def update(self, tariff, bonus_coef):
        query = self.table.update().\
            where(self.table.c.tariff == tariff).\
            values({'bonuscoef': bonus_coef})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class CardTypeInfo:
    '''
        Інформація та методи
        для таблиці CardInfo
    '''
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('cardtypeinfo', self.metadata,
                           Column('cardtype', VARCHAR(40), primary_key=True),
                           Column('creditlimit', Float, nullable=False),
                           autoload=True, extend_existing=True)

    def get_all(self):
        result = self.session.query(self.table).all()
        return result

    def get_by_type(self, cardtype):
        select_stmt = select([self.table]).\
                      where(self.table.c.cardtype == cardtype)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, cardtype, credit_limit):

        query = self.table.insert().\
            values({'cardtype': cardtype,
                    'creditlimit': credit_limit})

        self.session.execute(query)
        self.session.commit()

    def delete(self, cardtype):
        query = self.table.delete().\
            where(self.table.c.cardtype == cardtype)

        self.session.execute(query)
        self.session.commit()

    def update(self, cardtype, credit_limit):
        query = self.table.update().\
            where(self.table.c.cardtype == cardtype).\
            values({'creditlimit': credit_limit})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class Card:
    '''
        Інформація та методи
        для таблиці Card
    '''
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('card', self.metadata,
                           Column('cardid', VARCHAR(40), primary_key=True),
                           Column('pin', VARCHAR(10), nullable=False),
                           Column('cvv', VARCHAR(10), nullable=False),
                           Column('cardtype', VARCHAR(40), ForeignKey('cardtypeinfo.cardtype')),
                           Column('tariff', VARCHAR(40), ForeignKey('cardinfo.tariff')),
                           Column('status', VARCHAR(40), nullable=False),
                           Column('releasedate', DateTime, nullable=False),
                           Column('validitydate', DateTime, nullable=False),
                           Column('moneyamount', Float, nullable=False),
                           Column('creditlimit', Float, nullable=False),
                           Column('bonuses', VARCHAR(40), nullable=False),
                           Column('accountid', VARCHAR(40), ForeignKey('clientacclog.accountid')),
                           autoload=True, extend_existing=True)

    def get_by_accid(self, accid):
        select_stmt = select([self.table]).\
                      where(self.table.c.accountid == accid).\
                      order_by(desc(self.table.c.cardid))
        result = self.session.execute(select_stmt)
        return result

    def get_by_cardid(self, cardid):
        select_stmt = select([self.table]).\
                      where(self.table.c.cardid == cardid)
        result = self.session.execute(select_stmt)
        return result

    def get_money_by_cardid(self, cardid):
        select_stmt = select([self.table.c.moneyamount]).\
                      where(self.table.c.cardid == cardid)
        result = self.session.execute(select_stmt)
        return result

    def get_limit_by_cardid(self, cardid):
        select_stmt = select([self.table.c.creditlimit]).\
                      where(self.table.c.cardid == cardid)
        result = self.session.execute(select_stmt)
        return result

    def get_status_by_cardid(self, cardid):
        select_stmt = select([self.table.c.status]).\
                      where(self.table.c.cardid == cardid)
        result = self.session.execute(select_stmt)
        return result

    def get_name_surname_by_cardid(self, cardid, clientacclog, client):
        select_stmt = self.session.query(self.table,
                                         client.table.c.firstname,
                                         client.table.c.lastname).\
                      join(clientacclog.table,
                           self.table.c.accountid == clientacclog.table.c.accountid).\
                      join(client.table,
                           clientacclog.table.c.accountid == client.table.c.accountid).\
                      filter(self.table.c.cardid == cardid)
        result = self.session.execute(select_stmt)
        return result

    def get_bonuscoef_by_id(self, cardid, cardinfo):

        select_stmt = self.session.query(self.table, cardinfo.table.c.bonuscoef).\
                      join(cardinfo.table,
                           self.table.c.tariff == cardinfo.table.c.tariff).\
                      filter(self.table.c.cardid == cardid)
        result = self.session.execute(select_stmt)

        return result

    def insert(self, id, pin, cvv, type,
               tariff, status, rdate, vdate,
               money, limit, bonuses, acc_id):

        query = self.table.insert().\
            values({'cardid': id,
                    'pin': pin,
                    'cvv': cvv,
                    'cardtype': type,
                    'tariff': tariff,
                    'status': status,
                    'releasedate': rdate,
                    'validitydate': vdate,
                    'moneyamount': money,
                    'creditlimit': limit,
                    'bonuses': bonuses,
                    'accountid': acc_id})

        self.session.execute(query)
        self.session.commit()

    def delete(self, id):
        query = self.table.delete().\
            where(self.table.c.cardid == id)

        self.session.execute(query)
        self.session.commit()

    def update_card_status(self, id, status):

        query = self.table.update().\
            where(self.table.c.cardid == id).\
            values({'status': status})

        self.session.execute(query)
        self.session.commit()

    def update(self, id, pin, cvv, type,
               tariff, status, rdate, vdate,
               money, limit, bonuses, acc_id):

        query = self.table.update().\
            where(self.table.c.cardid == id).\
            values({'pin': pin,
                    'cvv': cvv,
                    'cardtype': type,
                    'tariff': tariff,
                    'status': status,
                    'releasedate': rdate,
                    'validitydate': vdate,
                    'moneyamount': money,
                    'creditlimit': limit,
                    'bonuses': bonuses,
                    'accountid': acc_id})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class TransInfo:
    '''
        Інформація та методи
        для таблиці TransInfo
    '''
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('transinfo', self.metadata,
                           Column('transactiontype', VARCHAR(40), primary_key=True),
                           Column('comissioncoef', Float, nullable=False),
                           autoload=True, extend_existing=True)

    def get_by_trans_type(self, trans_type):
        select_stmt = select([self.table.c.comissioncoef]).\
                      where(self.table.c.transactiontype == trans_type)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, type, comission_coef):

        query = self.table.insert().\
            values({'transactiontype': type,
                    'comissioncoef': comission_coef})

        self.session.execute(query)
        self.session.commit()

    def delete(self, type):
        query = self.table.delete().\
            where(self.table.c.transactiontype == type)

        self.session.execute(query)
        self.session.commit()

    def update(self, type, comission_coef):
        query = self.table.update().\
            where(self.table.c.transactiontype == type).\
            values({'comissioncoef': comission_coef})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class Transaction:
    '''
        Інформація та методи
        для таблиці Transaction
    '''
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('transaction', self.metadata,
                           Column('transactionid', Integer, primary_key=True),
                           Column('cardid', VARCHAR(40), ForeignKey('card.cardid')),
                           Column('cardidreciever', VARCHAR(40), nullable=False),
                           Column('initialsum', Float, nullable=False),
                           Column('comissionsum', Float, nullable=False),
                           Column('totalsum', Float, nullable=False),
                           Column('bonusesreсieved', Float, nullable=False),
                           Column('transdatetime', DateTime, nullable=False),
                           Column('transactiondescription', VARCHAR(120)),
                           Column('transactiontype', VARCHAR(80), ForeignKey('transinfo.transactiontype')),
                           autoload=True, extend_existing=True)

    def insert(self, cardid, rcardid, inisum,
               comsum, totsum, bonusesrec,
               transtime, transdesc, transtype):

        query = self.table.insert().\
            values({'cardid': cardid,
                    'cardidreciever': rcardid,
                    'initialsum': inisum,
                    'comissionsum': comsum,
                    'totalsum': totsum,
                    'transactiondescription': transdesc,
                    'bonusesreсieved': bonusesrec,
                    'transdatetime': transtime,
                    'transactiontype': transtype})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class TMPClientInf:
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('tmpclientinf', self.metadata,
                           Column('name',  VARCHAR(40), nullable=False),
                           Column('surname', VARCHAR(40), nullable=False),
                           Column('email', VARCHAR(40), nullable=False),
                           Column('passtype', VARCHAR(40), nullable=False),
                           Column('se_pass', VARCHAR(40), nullable=False),
                           Column('pass_id', VARCHAR(40)),
                           Column('ipn', VARCHAR(40), nullable=False),
                           Column('region', VARCHAR(40), nullable=False),
                           Column('city', VARCHAR(40), nullable=False),
                           Column('phone', VARCHAR(40), nullable=False),
                           Column('password', VARCHAR(40), nullable=False),
                           Column('question', VARCHAR(80), nullable=False),
                           Column('answer', VARCHAR(80), nullable=False),
                           Column('iban', VARCHAR(40), nullable=False),
                           Column('secret', VARCHAR(80), nullable=False),
                           autoload=True, extend_existing=True)

    def get_by_secret(self, secret):
        select_stmt = select([self.table]).\
                      where(self.table.c.secret == secret)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, name, surname, email, pass_type, se_pass,
               pass_id, ipn, region, city, phone, password,
               question, answer, iban, secret):

        query = self.table.insert().\
            values({'name': name,
                    'surname': surname,
                    'email': email,
                    'passtype': pass_type,
                    'se_pass': se_pass,
                    'pass_id': pass_id,
                    'ipn': ipn,
                    'region': region,
                    'city': city,
                    'phone': phone,
                    'password': password,
                    'question': question,
                    'answer': answer,
                    'iban': iban,
                    'secret': secret
                    })

        self.session.execute(query)
        self.session.commit()

    def delete(self, secret):
        query = self.table.delete().\
            where(self.table.c.secret == secret)

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class TMPCard:
    def __init__(self, session, meta):
        self.session = session
        self.metadata = meta
        self.table = Table('tmpcard', self.metadata,
                           Column('cardid', VARCHAR(40), nullable=False),
                           Column('pin', VARCHAR(10), nullable=False),
                           Column('cvv', VARCHAR(10), nullable=False),
                           Column('startdate', DateTime, nullable=False),
                           Column('enddate', DateTime, nullable=False),
                           Column('accountid', VARCHAR(40), nullable=False),
                           autoload=True, extend_existing=True)

    def get_by_accid(self, accid):
        select_stmt = select([self.table]).\
                      where(self.table.c.accountid == accid)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, id, pin, cvv, rdate, vdate, acc_id):

        query = self.table.insert().\
            values({'cardid': id,
                    'pin': pin,
                    'cvv': cvv,
                    'startdate': rdate,
                    'enddate': vdate,
                    'accountid': acc_id})

        self.session.execute(query)
        self.session.commit()

    def delete(self, accid):
        query = self.table.delete().\
            where(self.table.c.accountid == accid)

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()

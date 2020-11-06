from sqlalchemy import Table, MetaData, Column, VARCHAR, Float, DateTime, Integer, ForeignKey
from dao.PostgresDB import *


class ClientAccLog:
    '''
        Інформація та методи
        для таблиці ClientAccLog
    '''
    def __init__(self):
        self.db = PostgresDb()
        self.session = self.db.sqlalchemy_session
        self.metadata = MetaData(bind=self.db.sqlalchemy_engine)
        self.table = Table('clientacclog', self.metadata,
                           Column('accountid', VARCHAR(80), primary_key=True),
                           Column('accountstatus', VARCHAR(40), nullable=False),
                           autoload=True)

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
    def __init__(self):
        self.db = PostgresDb()
        self.session = self.db.sqlalchemy_session
        self.metadata = MetaData(bind=self.db.sqlalchemy_engine)
        self.table = Table('userlogins', self.metadata,
                           Column('userid', Integer, primary_key=True, autoincrement=True),
                           Column('userlogin', VARCHAR(40), primary_key=True),
                           Column('userpassword', VARCHAR(40), nullable=False),
                           Column('usersecurityanswer', VARCHAR(40), nullable=False),
                           Column('usersecurityquestion', VARCHAR(80), nullable=False),
                           Column('accountid', VARCHAR(40), ForeignKey('clientacclog.accountid')),
                           autoload=True)

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
    def __init__(self):
        self.db = PostgresDb()
        self.session = self.db.sqlalchemy_session
        self.metadata = MetaData(bind=self.db.sqlalchemy_engine)
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
                           autoload=True)

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

    def insert(self, acc_id, name, surname, city, region, pass_type, pass_id, ipn, phone):

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

    def update(self, acc_id, name, surname, city, region, pass_type, pass_id, ipn, phone):
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
    def __init__(self):
        self.db = PostgresDb()
        self.session = self.db.sqlalchemy_session
        self.metadata = MetaData(bind=self.db.sqlalchemy_engine)
        self.table = Table('cardinfo', self.metadata,
                           Column('tariff', VARCHAR(40), primary_key=True),
                           Column('bonuscoef', Float, nullable=False),
                           Column('creditlimit', Float, nullable=False),
                           autoload=True)

    def get_all(self):
        result = self.session.query(self.table).all()
        return result

    def get_by_tariff(self, tariff):
        select_stmt = select([self.table]).\
                      where(self.table.c.tariff == tariff)
        result = self.session.execute(select_stmt)
        return result

    def insert(self, tariff, bonus_coef, credit_limit):

        query = self.table.insert().\
            values({'tariff': tariff,
                    'bonuscoef': bonus_coef,
                    'creditlimit': credit_limit})

        self.session.execute(query)
        self.session.commit()

    def delete(self, tariff):
        query = self.table.delete().\
            where(self.table.c.tariff == tariff)

        self.session.execute(query)
        self.session.commit()

    def update(self, tariff, bonus_coef, credit_limit):
        query = self.table.update().\
            where(self.table.c.tariff == tariff).\
            values({'bonuscoef': bonus_coef,
                    'creditlimit': credit_limit})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()


class Card:
    '''
        Інформація та методи
        для таблиці Card
    '''
    def __init__(self):
        self.db = PostgresDb()
        self.session = self.db.sqlalchemy_session
        self.metadata = MetaData(bind=self.db.sqlalchemy_engine)
        self.table = Table('card', self.metadata,
                           Column('cardid', VARCHAR(40), primary_key=True),
                           Column('pin', VARCHAR(10), nullable=False),
                           Column('cvv', VARCHAR(10), nullable=False),
                           Column('cardtype', VARCHAR(40), nullable=False),
                           Column('tariff', VARCHAR(40), ForeignKey('cardinfo.tariff')),
                           Column('status', VARCHAR(40), nullable=False),
                           Column('releasedate', DateTime, nullable=False),
                           Column('validitydate', DateTime, nullable=False),
                           Column('moneyamount', Float, nullable=False),
                           Column('creditlimit', Float, nullable=False),
                           Column('bonuses', VARCHAR(40), nullable=False),
                           Column('accountid', VARCHAR(40), ForeignKey('clientacclog.accountid')),
                           autoload=True)

    def insert(self, id, pin, cvv, type, tariff, status, rdate, vdate, money, limit, bonuses, acc_id):

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

    def update(self, id, pin, cvv, type, tariff, status, rdate, vdate, money, limit, bonuses, acc_id):
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
    def __init__(self):
        self.db = PostgresDb()
        self.session = self.db.sqlalchemy_session
        self.metadata = MetaData(bind=self.db.sqlalchemy_engine)
        self.table = Table('transinfo', self.metadata,
                           Column('transactiontype', VARCHAR(40), primary_key=True),
                           Column('comissioncoef', Float, nullable=False),
                           autoload=True)

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
    def __init__(self):
        self.db = PostgresDb()
        self.session = self.db.sqlalchemy_session
        self.metadata = MetaData(bind=self.db.sqlalchemy_engine)
        self.table = Table('transaction', self.metadata,
                           Column('transactionid', Integer, primary_key=True),
                           Column('cardid', VARCHAR(40), ForeignKey('card.cardid')),
                           Column('cardidreciever', VARCHAR(40), nullable=False),
                           Column('initialsum', Float, nullable=False),
                           Column('comissionsum', Float, nullable=False),
                           Column('bonusesused', Float, nullable=False),
                           Column('totalsum', Float, nullable=False),
                           Column('bonusesreсieved', Float, nullable=False),
                           Column('transdatetime', DateTime, nullable=False),
                           Column('transactiontype', VARCHAR(80), ForeignKey('transinfo.transactiontype')),
                           autoload=True)

    def insert(self, cardid, rcardid, inisum, comsum, totsum, bonusused, bonusesrec, transtime, transtype):

        query = self.table.insert().\
            values({'cardid': cardid,
                    'cardidreciever': rcardid,
                    'initialsum': inisum,
                    'comissionsum': comsum,
                    'totalsum': totsum,
                    'bonusesused': bonusused,
                    'bonusesreсieved': bonusesrec,
                    'transdatetime': transtime,
                    'transactiontype': transtype})

        self.session.execute(query)
        self.session.commit()

    def __del__(self):
        self.session.close()

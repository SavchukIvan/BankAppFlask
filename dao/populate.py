from table_methods import *
from sqlalchemy import MetaData
# from PostgresDB import *

# db = PostgresDb()
# session = db.sqlalchemy_session
# metadata = MetaData(bind=db.sqlalchemy_engine)

# clg = ClientAccLog(session=session, meta=metadata)
# usl = UserLogins(session=session, meta=metadata)
# clt = Client(session=session, meta=metadata)
# cdinf = CardInfo(session=session, meta=metadata)
# ctinf = CardTypeInfo(session=session, meta=metadata)
# crd = Card(session=session, meta=metadata)
# tnf = TransInfo(session=session, meta=metadata)
# tact = Transaction(session=session, meta=metadata)
'''
    test operations for ClientAccLog
'''
# clg = ClientAccLog()
# clg.insert(id="UA133555678765132",
#            status="active")
# clg.update(id="UA133555678765132",
#            status="blocked")
# clg.delete(id="UA133555678765132")

'''
    test operations for UserLogins
'''
# usl = UserLogins(session=session, meta=metadata)
# result = usl.get_by_email(email="vanya.zombi2@gmail.com")
# print(result)
# usl.insert(login="app@bank.com",
#            password="Qweefd1233",
#            question="Mothers surname",
#            answer="Volkova",
#            acc_id="UA44305299000004000004485508896")
# usl.update(login="app@bank.com",
#            password="Qweefd1233",
#            question="Mothers surname",
#            answer="Petrovna",
#            acc_id="UA133555678765132")
# usl.delete(login="app@bank.com")

'''
    test operations for Client
'''
# clt = Client()

# result = clt.get_by_passid(pass_id="ТТ123456")
# ps = result.first()
# if ps is not None:
#     print(ps)
# else:
#     print('No passport found')
# result = clt.get_by_phone(phone="+380951601805")
# ph = result.first()
# if ph is not None:
#     print(ph)
# else:
#     print('No phone found')

# result = clt.get_by_ipn(ipn="1234567898")
# ipn = result.first()
# if ipn is not None:
#     print(ipn[-2])
# else:
#     print('No ipn found')
# clt.insert(acc_id="UA133555678765132",
#            name="Van",
#            surname="Darkholme",
#            city="Odessa",
#            region="Odessca obl",
#            pass_type="book",
#            pass_id="ТТ123456",
#            ipn="1234567890",
#            phone="+380951601805")
# clt.update(acc_id="UA133555678765132",
#            name="Van",
#            surname="Darkholme",
#            city="Odessa",
#            region="Odessca obl",
#            pass_type="book",
#            pass_id="TT123456",
#            ipn="1234567890",
#            phone="+380951601806")
# clt.delete(acc_id="UA133555678765132")

'''
    test operations for CardInfo
'''
# cdinf = CardInfo()
# cursor = cdinf.get_all()
# for i in cursor:
#     print(i)
# cdinf.insert(tariff='standard',
#              bonus_coef=0.01,
#              credit_limit=1000)
# cdinf.update(tariff='standard',
#              bonus_coef=0.011,
#              credit_limit=900)
# cdinf.delete(tariff='standard')

'''
test operations for Card
'''
# crd = Card()
# result = crd.get_by_accid(accid='UA44305299000004000004485508896')
# print(len(list(result)))
# inx = 0
# for index, card in enumerate(result):
#     print(index, card)
# crd.insert(id='1234567812345678',
#            pin='1234',
#            cvv='123',
#            type='credit',
#            tariff='Gold',
#            status='active',
#            rdate='28.10.2020',
#            vdate='28.10.2023',
#            money=0,
#            limit=1000,
#            bonuses=0,
#            acc_id='UA44305299000004000004485508896')
# crd.update(id='1234567812345678',
#            pin='1234',
#            cvv='123',
#            type='standard',
#            tariff='basic',
#            status='active',
#            rdate='28.10.2020',
#            vdate='28.10.2023',
#            money=0,
#            limit=900,
#            bonuses=0,
#            acc_id='UA133555678765132')
# crd.delete(id='UA133555678765132')

'''
    test operations for TransInfo
'''
# tnf = TransInfo()
# tnf.insert(type='basic', comission_coef=0.01)
# tnf.update(type='basic', comission_coef=0.02)
# tnf.delete(type='basic')

'''
    test operations for Transaction
'''
# import pandas as pd
# import numpy as np
# import random
# import datetime

# db = PostgresDb()
# # session = db.sqlalchemy_session
# # metadata = MetaData(bind=db.sqlalchemy_engine)
# cursor = db.execute(
# '''
# WITH USER_CARDS AS (
# 	SELECT CARDID
# 	FROM CARD
# 	WHERE ACCOUNTID = 'UA44305299000004000007652499398'
# )
# SELECT
# 	CASE 
# 	   WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN totalsum
#        ELSE TNC.INITIALSUM END
#        AS money_history,
# 	CASE
# 	   WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN 'sender'
#        ELSE 'getter' END
#        AS user_status,
#     CASE
#        WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN TNC.CARDID
#        ELSE TNC.CARDIDRECIEVER END
#        AS CARDID,
# 	TNC.TRANSDATETIME
# FROM TRANSACTION AS TNC
# WHERE (TNC.CARDID IN (SELECT * FROM USER_CARDS))
# OR (TNC.CARDIDRECIEVER IN (SELECT * FROM USER_CARDS))
# ORDER BY TNC.TRANSDATETIME;
# '''
# )

# ids = []
# money = []
# status = []
# time = []

# for row in cursor:
#     ids.append(row[2])
#     money.append(row[0])
#     status.append(row[1])
#     time.append(row[3].date())

# df = pd.DataFrame({'id': ids,
#                    'money': money,
#                    'status': status,
#                    'time': time})
# print(df)
# result = df.groupby(by=['id', 'status', 'time'])['money'].\
#             aggregate('sum').\
#             reset_index().\
#             sort_values(by=['time'])

# df_selected = result[result['time'] > datetime.datetime.now().date() - pd.to_timedelta("90day")].\
#                         reset_index(drop=True).\
#                         sort_values(by=['time'])

# print((df_selected["time"][len(df_selected)-1] - df_selected["time"][0]).days)
# if (df_selected["time"][len(df_selected)-1] - df_selected["time"][0]).days < 90:
#     print(False)

# cursor = db.execute(
# '''
# SELECT SUM(MONEYAMOUNT)
# FROM CARD
# WHERE ACCOUNTID = 'UA44305299000004000007652499398'
# '''
# )

# money_now = [row[0] for row in cursor][0]

# history = [money_now]


# for i in range(len(df_selected)-1, -1, -1):
#     status = df_selected.loc[i, 'status']
#     if status == 'sender':
#         val = history[0] + df_selected.loc[i, 'money']
#         history.insert(0, val)
#     elif status == 'getter':
#         val = history[0] - df_selected.loc[i, 'money']
#         history.insert(0, val)

# import matplotlib.pyplot as plt
# plt.plot([i for i in range(len(history))], history)
# plt.show()
# part_card = result[result['id'] == '4000009111787308'].\
#                         reset_index(drop=True).\
#                         sort_values(by=['time'])
# # print(result)

# df_selected = part_card[part_card['time'] > datetime.datetime.now().date() - pd.to_timedelta("90day")].\
#                         reset_index(drop=True).\
#                         sort_values(by=['time'])
# print(df_selected)
# dates_eu = pd.date_range(start='09-2-2020', end='12-1-2020', freq='D')
# dates_eu = date_rng.strftime('%d/%m/%Y')  # європейський час
# arr = np.array([0, 14216, 13743, 13334, 12929, 12713, 11950,
#                 11979, 11292, 10776, 10103, 9748, 8981, 8250, 7881, 7349, 
#                 6928, 6101, 5583, 4906, 4629, 4711, 4344, 3625, 2819, 2184,
#                 1646, 1173, 1266, 734, 366, 14771, 14004, 13387, 13032, 13163,
#                 12424, 11999, 11650, 11295, 10564, 9818, 9354, 8720, 8504, 7725,
#                 7429, 6913, 6280, 6280, 5869, 5653, 4825, 4293, 3874, 3078, 2985,
#                 2214, 1781, 1044, 325, 14679, 14163, 14207, 13470, 12664, 
#                 11889, 11445, 11001, 10205, 10183, 9774, 9470, 9102, 8274, 7528,
#                 7322, 7232, 6486, 5887, 5468, 4851, 4120, 3443, 3369, 3047,
#                 2603, 2182, 1830, 1412, 1029])

# current = 15000
# history = [current]

# for i in range(1, len(arr), 30):
#     print(arr[i])
    # history.insert(0, i - history[0])
# print(len(dates_eu))
# print(len(arr))

# init_sum = 15000
# rand_int0 = np.random.randint(200, 700, 90)

# rand_int = []

# for i in rand_int0:
#     rand_int.append(int(i))

# money_by_month = [0]
# tact = Transaction(session, metadata)
# sum_spend = 200
# tact.insert(
#     cardid='4000009111787308',
#     rcardid='4000002635819574',
#     inisum=sum_spend,
#     comsum=0.01*sum_spend,
#     totsum=sum_spend+0.01*sum_spend,
#     bonusesrec=sum_spend*0.001,
#     transtime='12-5-2020',
#     transdesc='For sweets',
#     transtype='transfer'
# )

# for i in range(len(rand_int)):
#     if ((i+1) % 7) == 0:
#         sum_spend = random.choice(rand_int)
#         sum_get = random.choice(rand_int)

#         tact.insert(
#             cardid='4000009111787308',
#             rcardid='4000002635819574',
#             inisum=sum_spend,
#             comsum=0.01*sum_spend,
#             totsum=sum_spend+0.01*sum_spend,
#             bonusesrec=sum_spend*0.001,
#             transtime=dates_eu[i],
#             transdesc='For sweets',
#             transtype='transfer'
#         )

#         tact.insert(
#             cardid='4000002635819574',
#             rcardid='4000009111787308',
#             inisum=sum_get,
#             comsum=0.01*sum_get,
#             totsum=sum_get+0.01*sum_get,
#             bonusesrec=sum_get*0.001,
#             transtime=dates_eu[i],
#             transdesc='For me',
#             transtype='transfer'
#         )

#     elif (i % 30) == 0:

#         sum_spend = random.choice(rand_int)
#         sum_get = 15000
#         tact.insert(
#             cardid='4000009111787308',
#             rcardid='4000002635819574',
#             inisum=sum_spend,
#             comsum=0.01*sum_spend,
#             totsum=sum_spend+0.01*sum_spend,
#             bonusesrec=sum_spend*0.001,
#             transtime=dates_eu[i],
#             transdesc='For sweets',
#             transtype='transfer'
#         )

#         tact.insert(
#             cardid='4000002635819574',
#             rcardid='4000009111787308',
#             inisum=sum_get,
#             comsum=0.01*sum_get,
#             totsum=sum_get+0.01*sum_get,
#             bonusesrec=sum_get*0.001,
#             transtime=dates_eu[i],
#             transdesc='For me',
#             transtype='transfer'
#         )
#     else:
#         sum_spend = random.choice(rand_int)
#         tact.insert(
#             cardid='4000009111787308',
#             rcardid='4000002635819574',
#             inisum=sum_spend,
#             comsum=0.01*sum_spend,
#             totsum=sum_spend+0.01*sum_spend,
#             bonusesrec=sum_spend*0.001,
#             transtime=dates_eu[i],
#             transdesc='For sweets',
#             transtype='transfer'
#         )


# print(history)
# print(len(history))


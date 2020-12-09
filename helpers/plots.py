import plotly
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import datetime
from plotly.subplots import make_subplots
import plotly.express as px
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.seasonal import STL


def pie_plot(labels, values, title):

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                 insidetextorientation='radial'
                                )])
    fig.update_layout(
            title=title,
            font=dict(
                family="Times New Roman",
                size=14,
                color="black"
            )
        )

    return plotly.io.to_html(fig, full_html=False)


def barchart_cards(labels, values, title):

    fig = go.Figure([go.Bar(x=labels, y=values)])

    fig.update_traces(marker_color='rgb(89, 172, 247)',
                      marker_line_color='rgb(0, 96, 139)',
                      marker_line_width=2,
                      opacity=0.9)

    fig.update_layout(
            title=title,
            font=dict(
                family="Times New Roman",
                size=14,
                color="black"
            )
        )

    return plotly.io.to_html(fig, full_html=False)


def plot_season_stl(db, accountid):

    cursor = db.execute(
    f'''
    WITH USER_CARDS AS (
        SELECT CARDID
        FROM CARD
        WHERE ACCOUNTID = '{accountid}'
    )
    SELECT
        CASE 
        WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN totalsum
        ELSE TNC.INITIALSUM END
        AS money_history,
        CASE
        WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN 'sender'
        ELSE 'getter' END
        AS user_status,
        CASE
        WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN TNC.CARDID
        ELSE TNC.CARDIDRECIEVER END
        AS CARDID,
        TNC.TRANSDATETIME
    FROM TRANSACTION AS TNC
    WHERE (TNC.CARDID IN (SELECT * FROM USER_CARDS))
    OR (TNC.CARDIDRECIEVER IN (SELECT * FROM USER_CARDS))
    ORDER BY TNC.TRANSDATETIME;
    '''
    )

    ids = []
    money = []
    status = []
    time = []

    for row in cursor:
        ids.append(row[2])
        money.append(row[0])
        status.append(row[1])
        time.append(row[3].date())

    if len(time) == 0 or (datetime.datetime.now().date() - time[0]).days < 60:
        return False

    date_rng = pd.date_range(start=datetime.datetime.now().date() - pd.to_timedelta("91day"),
                             end=datetime.datetime.now().date(),
                             freq='D')

    for i in range(len(date_rng)-1):
        if date_rng[i] not in time:
            money.insert(i, 0)
            time.insert(i, date_rng[i].date())
            status.insert(i, 'getter')
            ids.insert(i, ids[-1])

    df = pd.DataFrame({'id': ids,
                       'money': money,
                       'status': status,
                       'time': time})

    df_selected = df[df['time'] > datetime.datetime.now().date() - pd.to_timedelta("91day")].\
                            reset_index(drop=True).\
                            sort_values(by=['time'])

    cursor = db.execute(
    f'''
    SELECT SUM(MONEYAMOUNT)
    FROM CARD
    WHERE ACCOUNTID = '{accountid}'
    '''
    )

    money_now = [row[0] for row in cursor][0]

    history = [money_now]

    for i in range(89, -1, -1):
        status = df_selected.loc[i, 'status']
        if status == 'sender':
            val = history[0] + df_selected.loc[i, 'money']
            history.insert(0, val)
        else:
            val = history[0] - df_selected.loc[i, 'money']
            history.insert(0, val)

    result = seasonal_decompose(history, model='additive', period=30)

    fig = plotly.subplots.make_subplots(rows=4, cols=1)

    fig.add_scatter(y=history, name='your money', mode="lines",
                    line=dict(width=3, color="#3366CC"),
                    row=1, col=1)

    fig.add_scatter(y=result.trend, name='trendline', mode="lines",
                    line=dict(width=3),
                    row=2, col=1)

    fig.add_scatter(y=result.seasonal, name='seasonal', mode="lines",
                    line=dict(width=3),
                    row=3, col=1)

    fig.add_scatter(y=result.resid, name='residuals', mode="markers",
                    marker=dict(size=8),
                    row=4, col=1)

    fig.update_layout(
            title='Аналітика вашого профілю за 90 днів',
            font=dict(
                family="Times New Roman",
                size=14,
                color="black"
            )
        )

    return plotly.io.to_html(fig, full_html=False)


def plot_linear_regression(db, accountid, cardid):

    cursor = db.execute(
    f'''
    WITH USER_CARDS AS (
        SELECT CARDID
        FROM CARD
        WHERE ACCOUNTID = '{accountid}'
        AND CARDID = '{cardid}'
    )
    SELECT
        CASE 
        WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN totalsum
        ELSE TNC.INITIALSUM END
        AS money_history,
        CASE
        WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN 'sender'
        ELSE 'getter' END
        AS user_status,
        CASE
        WHEN TNC.CARDID IN (SELECT * FROM USER_CARDS) THEN TNC.CARDID
        ELSE TNC.CARDIDRECIEVER END
        AS CARDID,
        TNC.TRANSDATETIME
    FROM TRANSACTION AS TNC
    WHERE (TNC.CARDID IN (SELECT * FROM USER_CARDS))
    OR (TNC.CARDIDRECIEVER IN (SELECT * FROM USER_CARDS))
    ORDER BY TNC.TRANSDATETIME;
    '''
    )

    ids = []
    money = []
    status = []
    time = []

    for row in cursor:
        ids.append(row[2])
        money.append(row[0])
        status.append(row[1])
        time.append(row[3].date())

    if len(time) == 0 or (datetime.datetime.now().date() - time[0]).days < 3:
        return False

    date_rng = pd.date_range(start=datetime.datetime.now().date() - pd.to_timedelta("7day"),
                             end=datetime.datetime.now().date(),
                             freq='D')

    for i in range(len(date_rng)-1):
        if date_rng[i] not in time:
            money.insert(i, 0)
            time.insert(i, date_rng[i].date())
            status.insert(i, 'getter')
            ids.insert(i, ids[-1])

    df = pd.DataFrame({'id': ids,
                       'money': money,
                       'status': status,
                       'time': time})

    result = df.groupby(by=['id', 'status', 'time'])['money'].\
                aggregate('sum').\
                reset_index().\
                sort_values(by=['time'])

    df_selected = result[result['time'] > datetime.datetime.now().date() - pd.to_timedelta("7day")].\
                            reset_index(drop=True).\
                            sort_values(by=['time'])

    cursor = db.execute(
    f'''
    SELECT MONEYAMOUNT
    FROM CARD
    WHERE CARDID = '{cardid}'
    '''
    )

    money_now = [row[0] for row in cursor][0]

    history = [money_now]

    for i in range(6, -1, -1):
        if i == 0:
            break
        status = df_selected.loc[i, 'status']
        if status == 'sender':
            val = history[0] + df_selected.loc[i, 'money']
            history.insert(0, val)
        elif status == 'getter':
            val = history[0] - df_selected.loc[i, 'money']
            history.insert(0, val)

    df = pd.DataFrame({'x': [i for i in range(len(history))],
                       'y': history})

    X = df.x.values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, df.y)

    x_range = np.linspace(df.x.min(), df.x.max(), 20)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x='x', y='y', opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='тренд'))

    if model.coef_[0] > 1:
        fig.update_layout(
            title='За останні 7 днів, ваші статки ростуть!',
            font=dict(
                family="Times New Roman",
                size=14,
                color="black"
            )
        )
    elif model.coef_[0] == 1:
        fig.update_layout(
            title='За останні 7 днів, в вашому житті все стабільно!',
            font=dict(
                family="Times New Roman",
                size=14,
                color="black"
            )
        )
    else:
        fig.update_layout(
            title='За останні 7 днів, ваші статки зменшуються!',
            font=dict(
                family="Times New Roman",
                size=14,
                color="black"
            )
        )

    return plotly.io.to_html(fig, full_html=False)


def plot_activity(db):

    cursor = db.execute(
    '''
    SELECT DATE(TRANSDATETIME), COUNT(*)
    FROM TRANSACTION
    WHERE TRANSDATETIME <= NOW()
    AND TRANSDATETIME > NOW() - INTERVAL '31 DAYS'
    GROUP BY DATE(TRANSDATETIME)
    ORDER BY DATE(TRANSDATETIME);
    '''
    )

    time = []
    num = []

    for row in cursor:
        time.append(row[0])
        num.append(row[1])

    date_rng = pd.date_range(start=datetime.datetime.now().date() - pd.to_timedelta("30day"),
                             end=datetime.datetime.now().date(),
                             freq='D')

    print(date_rng)
    history = []
    k = 0
    for i in range(len(date_rng)-1):
        if date_rng[i] in time:
            k += 1
            history.append(num[time.index(time[k])])
        else:
            history.append(0)

    fig = go.Figure([go.Bar(x=[i for i in range(len(history))], y=history)])

    fig.update_traces(marker_color='rgb(89, 172, 247)',
                      marker_line_color='rgb(0, 96, 139)',
                      marker_line_width=2,
                      opacity=0.9)

    fig.update_layout(
            title='Активність транзакцій за останні 30 днів',
            font=dict(
                family="Times New Roman",
                size=14,
                color="black"
            )
        )

    return plotly.io.to_html(fig, full_html=False)


if __name__ == "__main__":
    # labels = ['standard','premium']
    # values = [4500, 1300]
    # title = 'Відношення тарифів карток в системі'
    # labels1 = ['debit', 'credit']
    # values1 = [2330, 1300]
    # title1 = 'Відношення типів карток в системі'
    # print(pie_plot(labels=labels, values=values, title=title))
    # pie_plot(labels=labels1, values=values1, title=title1)

    arr = np.array([0, 14216, 13743, 13334, 12929, 12713, 11950,
                    11979, 11292, 10776, 10103, 9748, 8981, 8250, 7881, 7349, 
                    6928, 6101, 5583, 4906, 4629, 4711, 4344, 3625, 2819, 2184,
                    1646, 1173, 1266, 734, 366, 14771, 14004, 13387, 13032, 13163,
                    12424, 11999, 11650, 11295, 10564, 9818, 9354, 8720, 8504, 7725,
                    7429, 6913, 6280, 6280, 5869, 5653, 4825, 4293, 3874, 3078, 2985,
                    2214, 1781, 1044, 325, 14679, 14163, 14207, 13470, 12664, 
                    11889, 11445, 11001, 10205, 10183, 9774, 9470, 9102, 8274, 7528,
                    7322, 7232, 6486, 5887, 5468, 4851, 4120, 3443, 3369, 3047,
                    2603, 2182, 1830, 1412, 1029])

    plot_season_stl(values=arr)
    # labels = ['card1', 'card2', 'card3', 'card4']
    # values = [1000, 1500, 2000, 0]
    # title = 'Баланс на ваших картках'
    # barchart_cards(labels, values, title)

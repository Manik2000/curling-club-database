import os
from datetime import datetime as dt

import pandas as pd
from dateutil.relativedelta import relativedelta


def generate_regular_payments(table, data, id_name, start, end, freq, amount, direction, period='M'):
    data = data.copy()

    def const_column(name, value):

        if not isinstance(value, str):
            data[name] = value

            return name

        return value

    end = const_column('end', end)
    freq = const_column('freq', freq)
    amount = const_column('amount', amount)

    def generate_payments(source):

        payment = pd.DataFrame()

        finish = dt.now() if pd.isnull(source[end]) else source[end]
        payment['date'] = pd.date_range(source[start], finish, freq=str(source[freq]) + period)
        payment['date'] = payment.date.dt.date
        payment['amount'] = direction * source[amount]
        payment[id_name] = source[id_name]

        return payment

    payments = pd.concat(list(data.apply(generate_payments, axis=1)))
    payments.index = pd.RangeIndex(1, len(payments) + 1)

    path = os.path.join('csv', f'{table}.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        df = pd.concat([df, pd.DataFrame(payments)])
    else:
        df = pd.DataFrame(payments)

    df.index = pd.RangeIndex(1, len(df) + 1)
    df['payment_id'] = df.index
    df.to_csv(path, index=False)

    return df


def generate_financial_info():

    def get_path(table):
        return os.path.join('csv', f'{table}.csv')
    
    table = 'finance'

    if os.path.exists(get_path(table)):
        os.remove(get_path(table))

    sponsors = pd.read_csv(get_path('sponsors'))
    generate_regular_payments(table, sponsors, 'sponsor_id', 'sign_date', 'expiry_date',
                              'frequency', 'amount', 1)

    management = pd.merge(pd.read_csv(get_path('management')), pd.read_csv(get_path('salaries')), on='management_id')
    coaches = pd.merge(pd.read_csv(get_path('coaches')), pd.read_csv(get_path('salaries')), on='coach_id')
    salaries = pd.concat([management, coaches])

    generate_regular_payments(table, salaries, 'salary_id', 'join_date', 'retire_date', 1, 'salary', -1)

    fee = 1000
    players = pd.read_csv(get_path('players'))
    generate_regular_payments(table, players, 'player_id', 'join_date', 'retire_date', 1, fee, 1)

    teams = pd.read_csv(get_path('teams'))
    equipment = pd.merge(pd.read_csv(get_path('equipment')), teams, on='team_code')

    generate_regular_payments(table, equipment, 'gear_id', 'established', dt.now(),
                              999, 'total_price', -1)

import os
from datetime import date
from datetime import datetime as dt

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


NAMES = {}
with open(os.path.join('txt', 'names', '100female_names.txt'), 'r', encoding='utf-8') as f_names:
    NAMES['female'] = f_names.read().split('\n')
with open(os.path.join('txt', 'names', '100male_names.txt'), 'r', encoding='utf-8') as m_names:
    NAMES['male'] = m_names.read().split('\n')

SURNAMES = {}
with open(os.path.join('txt', 'names', '100female_surnames.txt'), 'r', encoding='utf-8') as f_surnames:
    SURNAMES['female'] = f_surnames.read().split('\n')
with open(os.path.join('txt', 'names', '100male_surnames.txt'), 'r', encoding='utf-8') as m_surnames:
    SURNAMES['male'] = m_surnames.read().split('\n')


def generate_role(table, id_name, start_date, salary, freq, *team_codes, role=None, monthly_growth=.01 / 12,
                  start_born_year=1960, end_born_year=1980):
    def draw_person():

        gender = np.random.choice(['female', 'male'])
        return np.random.choice(NAMES[gender]), np.random.choice(SURNAMES[gender])

    def to_date(data, *columns):

        for column in columns:
            try:
                data[column] = data[column].dt.date
            except AttributeError:
                pass

        return data

    people = []

    t = start_date
    while t <= dt.now():

        first_name, last_name = draw_person()
        phone_number = '+48' + ''.join([str(np.random.randint(10)) for _ in range(9)])
        months = (t.year - start_date.year) * 12 + t.month - start_date.month
        salary = np.random.gamma(salary * (1 + months * monthly_growth))
        born = date(np.random.randint(start_born_year, end_born_year + 1), np.random.randint(1, 13),
                    np.random.randint(1, 28))
        join_date = t
        retire_date = t + relativedelta(months=int(round(np.random.exponential(freq))))
        t = retire_date
        retire_date = retire_date if retire_date <= dt.now() else np.nan

        if len(team_codes) > 0:
            for team_code in team_codes:
                person = {'team_code': team_code, 'first_name': first_name, 'last_name': last_name, 'salary': salary,
                          'phone_number': phone_number,
                          'born': born, 'join_date': join_date, 'retire_date': retire_date}
                if role:
                    person['role'] = role
                people.append(person)
        else:
            person = {'first_name': first_name, 'last_name': last_name, 'role': role, 'salary': salary,
                      'phone_number': phone_number,
                      'born': born, 'join_date': join_date, 'retire_date': retire_date}
            if role:
                person['role'] = role
            people.append(person)

    path = os.path.join('csv', f'{table}.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        df = pd.concat([df, to_date(pd.DataFrame(people), 'join_date', 'retire_date')])
    else:
        df = to_date(pd.DataFrame(people), 'join_date', 'retire_date')

    df.index = pd.RangeIndex(1, len(df) + 1)
    df[id_name] = df.index
    df.to_csv(path, index=False)

    return df


def generate_employees():

    def get_codes(league):
        path = os.path.join('txt', f'teams_{league}/team_codes_{league}.txt')
        with open(path, 'r') as team_codes:
            all_codes = team_codes.read().split('\n')
            return list(filter(lambda code: code.split(' ')[0] == 'CM', all_codes))


    employees_per_club = [
        {'role': 'President', 'count': 1, 'salary': 8000, 'freq': 12 * 12, 'start': '01/2000'},
        {'role': 'Vicepresident', 'count': 2, 'salary': 7000, 'freq': 12 * 10, 'start': '01/2000'},
        {'role': 'Accountant', 'count': 1, 'salary': 5000, 'freq': 12 * 6, 'start': '01/2000'},
        {'role': 'Press Spokesperson', 'count': 1, 'salary': 5000, 'freq': 12 * 5, 'start': '01/2005'},
        {'role': 'Secretary', 'count': 2, 'salary': 4500, 'freq': 12 * 6, 'start': '01/2000'},
        {'role': 'Social Media Manager', 'count': 1, 'salary': 3500, 'freq': 12 * 4, 'start': '01/2010'},
        {'role': 'CEO', 'count': 1, 'salary': 6500, 'freq': 12 * 8, 'start': '01/2008'},
        {'role': 'CTO', 'count': 1, 'salary': 6000, 'freq': 12 * 6, 'start': '01/2008'},
        {'role': 'COO', 'count': 1, 'salary': 6000, 'freq': 12 * 6, 'start': '01/2008'},
        {'role': 'CMO', 'count': 1, 'salary': 6000, 'freq': 12 * 6, 'start': '01/2012'},
        {'role': 'CFO', 'count': 1, 'salary': 6000, 'freq': 12 * 6, 'start': '01/2012'},
        {'role': 'Audit Committee Chairman', 'count': 1, 'salary': 7000, 'freq': 12 * 8, 'start': '01/2006'},
        {'role': 'Audit Committee Secretary', 'count': 1, 'salary': 4500, 'freq': 12 * 6, 'start': '01/2006'},
        {'role': 'Audit Committee Member', 'count': 2, 'salary': 4000, 'freq': 12 * 4, 'start': '01/2006'}
    ]

    coach = {'count': 1, 'salary': 5500, 'freq': 12 * 4, 'start': '01/2000'}

    PLM = get_codes('PLM')
    PLK = get_codes('PLK')
    MPJ = get_codes('MPJ')
    all_codes = PLM + PLK + MPJ

    management_table = 'management'
    coach_table = 'coaches'

    management_id = 'management_id'
    coach_id = 'coach_id'

    management_path = os.path.join('csv', f'{management_table}.csv')
    if os.path.exists(management_path):
        os.remove(management_path)

    coach_path = os.path.join('csv', f'{coach_table}.csv')
    if os.path.exists(coach_path):
        os.remove(coach_path)

    def generate_for_club(role_dict):
        for _ in range(role_dict['count']):
            df = generate_role(management_table, management_id, dt.strptime(role_dict['start'], '%m/%Y'),
                               role_dict['salary'], role_dict['freq'], role=role_dict['role'])

        return df

    def generate_coach(team_code, team_start, delay):
        for _ in range(coach['count']):
            df = generate_role(coach_table, coach_id,
                               max(dt.strptime(coach['start'], '%m/%Y'),
                                   dt.strptime(team_start, '%m/%Y') + relativedelta(years=delay)),
                               coach['salary'], coach['freq'], team_code)

        return df

    for employee in employees_per_club:
        generate_for_club(employee)

    for i, plm in enumerate(PLM):
        generate_coach(plm, '01/2000', 2 * i)

    for i, plk in enumerate(PLK):
        generate_coach(plk, '01/2006', 4 * i)

    for i, mpj in enumerate(MPJ):
        generate_coach(mpj, '01/2008', 3 * i)

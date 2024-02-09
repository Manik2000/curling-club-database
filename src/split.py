import os

import numpy as np
import pandas as pd


info_table = 'personal_info'
salary_table = 'salaries'
management_table = 'management'
coach_table = 'coaches'
player_table = 'players'
management_id = 'management_id'
coach_id = 'coach_id'
player_id = 'player_id'


def unique_key(table, key, first_const=3, draw=lambda: str(np.random.randint(10))):
    def new_key(key_value):
        random_position = np.random.randint(first_const, len(key_value))
        return key_value[:random_position] + draw() + key_value[random_position + 1:]

    mask = table.duplicated(subset=key)
    while sum(mask) > 0:

        for i, duplicate in table.loc[mask, :].iterrows():
            duplicate[key] = new_key(duplicate[key])

        mask = table.duplicated(subset=key)

    return table


def split_table(table, split_table, id_name, *columns, key=None):
    columns = list(columns)
    path = os.path.join('csv', f'/{table}.csv')
    df = pd.read_csv(path)
    split_df = df[columns]
    df.drop(columns=columns, inplace=True)

    split_path = os.path.join('csv', f'/{split_table}.csv')
    split_df[id_name] = df[id_name]
    if os.path.exists(split_path):
        split_df = pd.concat([split_df, pd.read_csv(split_path)])

    if key:
        split_df = unique_key(split_df, key)
    else:
        split_df.index = pd.RangeIndex(1, len(split_df) + 1)
        split_df['salary_id'] = split_df.index
    split_df.to_csv(split_path, index=False)
    df.to_csv(path, index=False)

    return df, split_df


def split_before_finance():
    salary_path = os.path.join('csv', f'/{salary_table}.csv')
    if os.path.exists(salary_path):
        os.remove(salary_path)
    salary_columns = ['salary']
    for table, id_name in zip((management_table, coach_table), (management_id, coach_id)):
        split_table(
            table,
            salary_table,
            id_name,
            *salary_columns
        )


def split_after_finance():
    info_path = os.path.join('csv', f'/{info_table}.csv')
    if os.path.exists(info_path):
        os.remove(info_path)

    info_key = 'phone_number'
    info_columns = ['phone_number', 'first_name', 'last_name', 'born', 'join_date', 'retire_date']

    for table, id_name in zip((management_table, coach_table, player_table),
                              (management_id, coach_id, player_id)):
        split_table(
            table,
            info_table,
            id_name,
            *info_columns,
            key=info_key
        )

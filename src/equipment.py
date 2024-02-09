import os

import numpy as np
import pandas as pd


def generate_items_table(item_name, rows, brands, models, *conditions, max_iter=100, **kwargs):
    if np.prod([len(values) for values in (brands, models)]) < rows:
        raise ValueError('Too many rows for distinct values.')

    def generate(iter_through, *conditional):

        i = 0
        df = pd.DataFrame()
        iter_through = list(iter_through)

        while len(df) < rows and i < max_iter:

            adds = pd.DataFrame({field: np.random.choice(values, size=rows - len(df))
                                 for field, values in iter_through})
            mask = np.array([True for _ in range(rows - len(df))])
            for condition in conditional:
                mask = np.logical_and(mask, condition(adds))
            df = pd.concat([df, adds[mask]])
            df.drop_duplicates(inplace=True)
            i += 1

        return df

    ids = generate(zip(['brand', 'model'], [brands, models]))
    properties = generate(kwargs.items(), *conditions)

    index = np.arange(rows)
    ids.index = index
    properties.index = index

    data = pd.concat([ids, properties], axis=1)
    data.index = pd.RangeIndex(1, len(data) + 1)
    data['id'] = data.index
    data.to_csv(os.path.join('csv', f'{item_name}.csv'), index=False)
    return data


foot_N = 4 * 9

foot_brands = ['Goldline', 'BalancePlus', 'Olson', 'Asham']
foot_models = ['Quantum', 'Swift', 'Classic', 'Genesis', 'NeoSport', 'Breeze', 'Velocity', 'Cyclone', 'Swagger', 'Delux']

foot_prices = list(range(350, 650, 10))
foot_fors = ['men', 'women', 'junior']
foot_weights = list(range(800, 1101, 10))
foot_colors = ['black', 'red', 'blue']
foot_sliders = ['full', 'split', 'pods']
foot_sizes = list(range(30, 50))


foot_for_size_cond = lambda df: (((df['purpose'] == 'men') & (df['size'] >= 40)) |
                            ((df['purpose'] == 'women') & (df['size'].between(35, 45))) |
                            ((df['purpose'] == 'junior') & (df['size'] <= 40)))
foot_for_price_cond = lambda df: ((((df['purpose'] == 'men') | (df['purpose'] == 'women')) & (df['price'] > 400)) |
                            ((df['purpose'] == 'junior') & (df['price'] < 500)))
foot_for_weight_cond = lambda df: (((df['purpose'] == 'men') & (df['weight'] >= 900)) |
                            ((df['purpose'] == 'women') & (df['weight'].between(850, 1050))) |
                            ((df['purpose'] == 'junior') & (df['weight'] <= 1000)))

foot_conditions = foot_for_size_cond, foot_for_price_cond, foot_for_weight_cond


brooms_N = 5 * 6

brooms_brands = ['Goldline', 'BalancePlus', 'Hardline', 'Olson', 'Asham']
brooms_models = ['Pyro', 'Specialty', 'Flash', 'Rebel', 'Tapered', 'Ultra', 'Flash']
brooms_fors = ['men', 'women', 'junior']
brooms_prices = list(range(400, 800, 10))
brooms_colors = ['black', 'red', 'blue', 'yellow', 'green', 'white']
brooms_materials = ['carbon fiber', 'composite', 'fiberlite']
brooms_heads = ['Air', 'Air X', 'Air Stationary']
brooms_pads = ['Air Pro', 'Airway']
brooms_sizes = [1, 1 + 1/16, 1 + 1/8]

brooms_for_size_cond = lambda df: ((df['purpose'] == 'junior') & (df['size'] != 1 + 1/8) |
                            (df['purpose'] != 'junior'))
brooms_material_price_cond = lambda df: (((df['material'] == 'carbon fiber') & (df['price'] < 550)) |
                                  ((df['material'] == 'composite') & (df['price'].between(400, 600))) |
                                  ((df['material'] == 'fiberlite') & (df['price'] > 500)))

brooms_conditions = brooms_for_size_cond, brooms_material_price_cond

hand_N = 4 * 5

hand_brands = ['Goldline', 'BalancePlus', 'Hardline', 'Asham']
hand_models = ['Endurance', 'Platinum', 'Litespeed', 'Precision', 'Thermocurl', 'Ultrafit']

hand_prices = list(range(80, 250, 5))
hand_colors = ['black', 'red', 'white']
hand_leathers = ['pig', 'lamb']
hand_lines = ['unlined', 'partially lined', 'fully lined']
hand_sizes = ['XS', 'S', 'M', 'L', 'XL']
hand_kinds = ['gloves', 'mitts']
hand_fors = ['men', 'women', 'unisex']

leather_price_cond = lambda df: (((df['leather'] == 'lamb') & (df['price'] > 150)) |
                                 ((df['leather'] == 'pig') & (df['price'] < 200)))

hand_conditions = leather_price_cond,

pants_N = 7 * 5

pants_brands = ['Goldline', 'BalancePlus', 'Hardline', 'Asham', 'Ultima', 'Tournament', 'Olson']
pants_models = ['Jean', 'Yoga', 'Dress', 'Classic', 'Vienna', 'Stockholm', 'Viola', 'Swedish']

pants_prices = list(range(250, 500, 10))
pants_fors = ['men', 'women']
pants_sizes = list(range(2, 16, 2))

pants_conditions = leather_price_cond,

head_N = 3 * 3

head_brands = ['Goldline', 'Ribcap', 'Asham']
head_models = ['Dylan', 'Harris', 'Lenny', 'visor']

head_prices = list(range(300, 400, 5))
head_fors = ['men', 'women', 'junior']
head_kinds = ['helmet', 'hat', 'toque']


def get_codes(league):
    path = os.path.join('..', 'txt', f'teams_{league}', f'team_codes_{league}.txt')
    with open(path, 'r') as team_codes:
        all_codes = team_codes.read().split('\n')
        return list(filter(lambda code: code.split(' ')[0] == 'CM', all_codes))


for_women = lambda df: df['purpose'] == 'women'
for_men = lambda df: df['purpose'] == 'men'
for_junior = lambda df: df['purpose'] == 'junior'


def generate_equipment_table():
    equipment = ['footwear', 'brooms', 'handwear', 'pants', 'headwear']

    table = 'equipment'
    path = os.path.join('csv', f'{table}.csv')

    def generate_table(table, team_code, player_items, player_conditions, min_players=6, max_players=12):
        data = {'team_code': team_code, 'quantity': np.random.randint(min_players, max_players + 1), 'total_price': 0}

        for item_name, condition in zip(player_items, player_conditions):
            items = pd.read_csv(os.path.join('csv', f'{item_name}.csv'))
            item = items[condition(items)].sample()
            data[f'{item_name}_id'] = item.id.values[0]
            data['total_price'] += item.price.values[0]

        data['total_price'] *= data['quantity']
        filename = os.path.join('csv', f'{table}.csv')
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            df = pd.concat([df, pd.DataFrame([data])])
        else:
            df = pd.DataFrame([data])

        df.index = pd.RangeIndex(1, len(df) + 1)
        df['gear_id'] = df.index
        df.to_csv(filename, index=False)

        return df

    if os.path.exists(path):
        os.remove(path)

    for plm in get_codes('PLM'):
        generate_table(table, plm, equipment, [for_men,
                                               for_men,
                                               lambda df: df['gender'].isin(('men', 'unisex')),
                                               lambda df: df['gender'] == 'men',
                                               for_men])

    for plk in get_codes('PLK'):
        generate_table(table, plk, equipment, [for_women,
                                               for_women,
                                               lambda df: df['gender'].isin(('women', 'unisex')),
                                               lambda df: df['gender'] == 'women',
                                               for_women])

    for mpj in get_codes('MPJ'):
        generate_table(table, mpj, equipment, [for_junior,
                                               for_junior,
                                               lambda df: df['gender'].isin(('men', 'unisex')),
                                               lambda df: df['gender'] == 'men',
                                               for_junior])
    df = pd.read_csv(path)

    return df

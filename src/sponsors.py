import os
from datetime import datetime as dt

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


def generate_sponsorship(start_date, sign_freq, expected_payments, sponsorship_amount, sponsorship_freq):
    with open(os.path.join('txt', 'sponsors', 'sponsor_names.txt'), 'r', encoding="utf-8") as sponsors:
        NAMES = sponsors.read().split('\n')

    sponsors = []

    t = start_date
    while len(NAMES) > 0:

        sponsor_name = np.random.choice(NAMES)
        NAMES.remove(sponsor_name)
        sign_date = t + relativedelta(months=int(round(np.random.exponential(sign_freq))))
        t = sign_date
        if sign_date > dt.now():
            break
        amount = np.random.gamma(sponsorship_amount)
        freq = int(round(np.random.exponential(sponsorship_freq - 1))) + 1
        payments = np.random.poisson(expected_payments)
        expiry_date = sign_date + relativedelta(months=int(freq * payments))
        expiry_date = expiry_date if expiry_date <= dt.now() else np.nan

        sponsors.append({'sponsor': sponsor_name, 'amount': amount, 'frequency': freq, 'sign_date': sign_date,
                         'expiry_date': expiry_date})

    path = os.path.join('csv', 'sponsors.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        df = pd.concat([df, pd.DataFrame(sponsors)])
    else:
        df = pd.DataFrame(sponsors)

    df.index = pd.RangeIndex(1, len(df) + 1)
    df['sponsor_id'] = df.index
    df.to_csv(path, index=False)

    return df

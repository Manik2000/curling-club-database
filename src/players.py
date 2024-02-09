import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from CONSTANTS import *


np.random.seed(10)


characteristics = {
    "men": dict(
        names=male_names,
        surnames=male_surnames,
        min_joining_age=20,
        max_joining_age=40
    ),
    "women": dict(
        names=female_names,
        surnames=female_surnames,
        min_joining_age=20,
        max_joining_age=40
    ),
    "junior": dict(
        names=male_names,
        surnames=male_surnames,
        min_joining_age=13,
        max_joining_age=17
    )
}


def date_fromiso(date):
    return datetime.fromisoformat(date).date()


def random_date(min_date, max_date):
    delta = (max_date - min_date).days
    date = (min_date + timedelta(np.random.randint(1, delta)))
    return date


def random_shooting_percentage():
    Z = np.random.normal(0.68, 0.12)
    Z_ = min([0.95, Z])
    _Z_ = max([0.2, Z_])
    return round(_Z_, 2)


def random_phone_number():
    first_digit = str(np.random.randint(6, 10))
    remaining_digits = ''.join(map(str, np.random.randint(0, 10, size=8)))
    digits = first_digit + remaining_digits
    return '48' + digits[:3] + digits[3:6] + digits[6:]


def draw_player(category, team_code, position, born, joined, max_years_in_club=10):
    params = characteristics[category]
    first_name = np.random.choice(params["names"])
    last_name = np.random.choice(params["surnames"])
    retired = joined + timedelta(np.random.randint(1*365, max_years_in_club*365))

    player = {
        "first_name": first_name,
        "last_name": last_name,
        "born": born,
        "phone_number": random_phone_number(),
        "team_code": team_code,
        "join_date": joined,
        "retire_date": retired,
        "position": position,
        "shooting_percentage": random_shooting_percentage(),
    }
    return player


def generate_players():
    all_players = []

    for team_code, establishment_date in establishment_dates.items():

        players = []
        category = categories[team_code]
        num_of_active_players = 0

        for position in position_names:

            min_joining_age = characteristics[category]["min_joining_age"]
            max_joining_age = characteristics[category]["max_joining_age"]

            offset = timedelta(np.random.randint(1, 60))  # 60 days after establishment
            signed = datetime.date(datetime.fromisoformat(establishment_date)) + offset
            born = random_date(signed - timedelta(max_joining_age*365), signed - timedelta(min_joining_age*365))

            player = draw_player(category,
                                team_code,
                                position,
                                born,
                                signed)

            if player["retire_date"] > starting_season:
                player["retire_date"] = np.nan

            players.append(player)

        retired_players = [player for player in players if player["retire_date"] is not np.nan]
        retired_players.sort(key=lambda player: player["retire_date"], reverse=True)

        while retired_players:
            first_retired = retired_players.pop()
            signed_offset = timedelta(np.random.randint(1, 30))  # 30 days after retirenment
            signed = first_retired["retire_date"] + signed_offset
            born = random_date(signed - timedelta(max_joining_age*365), signed - timedelta(min_joining_age*365))

            new_player = draw_player(category,
                                    team_code,
                                    first_retired["position"],
                                    born,
                                    signed)

            players.append(new_player)

            if new_player["retire_date"] < starting_season:
                retired_players.append(new_player)
            else:
                new_player["retire_date"] = np.nan

            retired_players.sort(key=lambda player: player["retire_date"], reverse=True)

        all_players.extend(players)
        players_df = pd.DataFrame(all_players).sort_values(by=["join_date"], ascending=True, ignore_index=True)
        players_df["player_id"] = pd.RangeIndex(1, len(players_df)+1)
        players_df = players_df[["player_id", *players_df.columns[:-1]]]

    players_df.to_csv(os.path.join("csv", "players.csv"), index=False)

    return players_df

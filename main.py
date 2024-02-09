import os
import warnings
from datetime import datetime as dt
from urllib.parse import quote_plus as urlquote

import pandas as pd
from sqlalchemy.engine import create_engine

from config import DATABASE, HOST, PASSWORD, USER
from CONSTANTS import leagues
from src.database_creator import create_tables, drop_tables
from src.employees import generate_employees
from src.equipment import *
from src.finance import generate_financial_info
from src.matches_and_teams import (all_matches_and_ends, generate_all_teams,
                                   generate_PLPM_teams)
from src.players import generate_players
from src.split import split_after_finance, split_before_finance
from src.sponsors import generate_sponsorship


def create_and_fill_database():
    os.mkdir("csv")

    drop_tables()
    create_tables()

    engine = create_engine(f'mysql+mysqlconnector://{USER}:%s@{HOST}/{DATABASE}' % urlquote(PASSWORD))

    def write_df_to_sql(dataframe, name):
        dataframe.to_sql(name, engine, if_exists="append")

    leagues.set_index("league_code", inplace=True)
    write_df_to_sql(leagues, "Leagues")

    players = generate_players()

    teams_PLPM = generate_PLPM_teams(players)

    teams = generate_all_teams(teams_PLPM)
    teams.set_index("team_code", inplace=True)
    write_df_to_sql(teams, "Teams")

    matches, ends = all_matches_and_ends(teams_PLPM)
    matches[["match_id", "matchweek",
             "total_red", "total_yellow"]] = matches[["match_id", "matchweek",
                                                      "total_red", "total_yellow"]].astype(np.float)
    matches.set_index("match_id", inplace=True)
    write_df_to_sql(matches, 'Matches')

    ends.set_index("end", inplace=True)
    write_df_to_sql(ends, "Ends")

    footwear = generate_items_table('footwear', foot_N, foot_brands, foot_models, *foot_conditions,
                                    price=foot_prices,
                                    purpose=foot_fors,
                                    weight=foot_weights,
                                    color=foot_colors,
                                    slider=foot_sliders,
                                    size=foot_sizes
                                    )
    footwear.set_index("id", inplace=True)
    write_df_to_sql(footwear, "Footwear")

    handwear = generate_items_table('handwear', hand_N, hand_brands, hand_models, *hand_conditions,
                                    price=hand_prices,
                                    gender=hand_fors,
                                    color=hand_colors,
                                    leather=hand_leathers,
                                    kind=hand_kinds,
                                    line=hand_lines,
                                    size=hand_sizes
                                    )
    handwear.set_index("id", inplace=True)
    write_df_to_sql(handwear, "Handwear")

    brooms = generate_items_table('brooms', brooms_N, brooms_brands, brooms_models, *brooms_conditions,
                                  price=brooms_prices,
                                  purpose=brooms_fors,
                                  color=brooms_colors,
                                  material=brooms_materials,
                                  head=brooms_heads,
                                  pad=brooms_pads,
                                  size=brooms_sizes)
    brooms.set_index("id", inplace=True)
    write_df_to_sql(brooms, "Brooms")

    pants = generate_items_table('pants', pants_N, pants_brands, pants_models,
                                 price=pants_prices,
                                 gender=pants_fors,
                                 size=pants_sizes
                                 )
    pants.set_index("id", inplace=True)
    write_df_to_sql(pants, "Pants")

    headwear = generate_items_table('headwear', head_N, head_brands, head_models,
                                    price=head_prices,
                                    purpose=head_fors,
                                    kind=head_kinds
                                    )
    headwear.set_index("id", inplace=True)
    write_df_to_sql(headwear, "Headwear")

    equipment = generate_equipment_table()
    equipment.set_index("gear_id", inplace=True)
    write_df_to_sql(equipment, "Equipment")

    club_start_date = '01/2000'
    sponsors = generate_sponsorship(dt.strptime(club_start_date, '%m/%Y'), 30, 40, 100000, 3)
    sponsors.set_index("sponsor_id", inplace=True)
    write_df_to_sql(sponsors, "Sponsors")

    generate_employees()
    split_before_finance()
    generate_financial_info()
    split_after_finance()

    players = pd.read_csv(os.path.join("csv", "players.csv"))
    players.set_index("player_id", inplace=True)
    write_df_to_sql(players, 'Players')

    management = pd.read_csv(os.path.join("csv", "management.csv"))
    management.set_index("management_id", inplace=True)
    write_df_to_sql(management, "Management")

    coaches = pd.read_csv(os.path.join("csv", "coaches.csv"))
    coaches.set_index("coach_id", inplace=True)
    write_df_to_sql(coaches, "Coaches")

    salaries = pd.read_csv(os.path.join("csv", "salaries.csv"))
    salaries.set_index("salary_id", inplace=True)
    write_df_to_sql(salaries, "Salaries")

    finance = pd.read_csv(os.path.join("csv", "finance.csv"))
    finance.set_index("payment_id", inplace=True)
    write_df_to_sql(finance, "Finance")

    personal_info = pd.read_csv(os.path.join("csv", "personal_info.csv"))
    personal_info.set_index("phone_number", inplace=True)
    write_df_to_sql(personal_info, "PersonalInfo")

    for csv_file in os.listdir("csv"):
        os.remove(os.path.join("csv", f"{csv_file}"))
    os.rmdir("csv")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    create_and_fill_database()

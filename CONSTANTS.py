import os
from datetime import datetime

import numpy as np
import pandas as pd


SEED = 10


def read_txt(category, file):
    return np.loadtxt(os.path.join("txt", category, f"{file}.txt"), dtype=str, delimiter='\n', encoding="utf-8")


position_names = ['L', 'SE', 'V', 'SK', 'AL', 'AL']
m_team_codes = ["CM PP", "CM SZ", "CM ST", "CM JY"]
f_team_codes = ["CM AA", "CM BB"]
jr_team_codes = ["CM FP", "CM BS"]

all_team_codes = [*m_team_codes,
                  *f_team_codes,
                  *jr_team_codes]

male_names = read_txt("names", "100male_names")
female_names = read_txt("names", "100female_names")
male_surnames = read_txt("names", "100male_surnames")
female_surnames = read_txt("names", "100female_surnames")

starting_season = datetime.date(datetime.fromisoformat('2020-10-11'))

establishment_dates = {
    "CM PP": "2000-01-01",
    "CM SZ": "2002-01-01",
    "CM ST": "2004-01-01",
    "CM JY": "2006-01-01",
    "CM AA": "2006-01-01",
    "CM FP": "2008-01-01",
    "CM BB": "2010-01-01",
    "CM BS": "2011-01-01",
}

categories = {}
for team_code in m_team_codes:
    categories[team_code] = "men"

for team_code in f_team_codes:
    categories[team_code] = "women"

for team_code in jr_team_codes:
    categories[team_code] = "junior"


stopdate = datetime.fromisoformat("2022-06-06")  # matches played up to that date

PLM_20_21_starting_days = ['2020-10-12', '2020-10-13']  # <------------------- monday, tuesday
PLK_20_21_starting_days = ['2020-11-04', '2020-11-05']  # <------------------- wednesday, thursday
MPJ_20_21_starting_days = ['2020-12-07', '2020-12-08', '2020-12-09']  # <----- monday, tuesday, wednesday
PLPM_20_21_starting_days = ['2020-11-06', '2020-11-07']  # <------------------- friday, saturday

PLM_21_22_starting_days = ['2021-10-11', '2021-10-12']  # <------------------- monday, tuesday
PLK_21_22_starting_days = ['2021-11-03', '2021-11-04']  # <------------------- wednesday, thursday
MPJ_21_22_starting_days = ['2021-12-06', '2021-12-07', '2021-12-08']  # <----- monday, tuesday, wednesday
PLPM_21_22_starting_days = ['2021-11-05', '2021-11-06']  # <------------------- friday, saturday

team_names_PLM = read_txt("teams_PLM", "team_names_PLM")
team_codes_PLM = read_txt("teams_PLM", "team_codes_PLM")
team_names_PLK = read_txt("teams_PLK", "team_names_PLK")
team_codes_PLK = read_txt("teams_PLK", "team_codes_PLK")
team_names_MPJ = read_txt("teams_MPJ", "team_names_MPJ")
team_codes_MPJ = read_txt("teams_MPJ", "team_codes_MPJ")

teams_PLM = pd.DataFrame({"team_code": team_codes_PLM, "team_name": team_names_PLM}, index=None)
teams_PLK = pd.DataFrame({"team_code": team_codes_PLK, "team_name": team_names_PLK}, index=None)
teams_MPJ = pd.DataFrame({"team_code": team_codes_MPJ, "team_name": team_names_MPJ}, index=None)

leagues = pd.DataFrame({"PLM": "Polska Liga Mężczyzn",
                        "PLK": "Polska Liga Kobiet",
                        "PLPM": "Polska Liga Par Mieszanych",
                        "MPJ": "Mistrzostwa Polski Juniorów"}.items(),
                       columns=["league_code", "league_name"])

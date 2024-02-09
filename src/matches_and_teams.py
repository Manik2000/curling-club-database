import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from CONSTANTS import *


def date_fromiso(date):
    return datetime.fromisoformat(date).date()


def random_date(min_date, max_date):
    delta = (max_date - min_date).days
    date = (min_date + timedelta(np.random.randint(1, delta)))
    return date


def read_txt(path):
    return np.loadtxt(os.path.join("txt", f"{path}.txt"), dtype=str, delimiter='\n', encoding="utf-8")


def round_robin(teams, week):
    """Round-robin tournament pairing algorithm"""
    teams = teams.copy()
    half = int(len(teams) / 2)
    teams[1:] = np.roll(teams[1:], week)
    teams[half:] = np.flip(teams[half:])
    pairs = np.transpose(teams.reshape([2, half]))
    return pairs


def assign_team_skill(team_codes, min_skill=0.8, max_skill=1, seed=42):
    np.random.seed(seed)
    skill = dict(zip(team_codes, np.random.uniform(min_skill, max_skill, size=len(team_codes))))
    return skill


def simulate_match(skill_red, skill_yel, ends=8):
    points_red = []
    points_yel = []

    for end in range(ends):

        if (ends - end) * 8 < np.abs(np.sum(points_red) - np.sum(points_yel)):  # no chance for comeback
            points_red.extend((ends - end) * [np.nan])  # skipping next ends
            points_yel.extend((ends - end) * [np.nan])  # skipping next ends
            break  # surrender

        Rs = np.random.uniform(0, skill_red, size=8)  # throw 8 stones (the closer the score is to 1, the better)
        Ys = np.random.uniform(0, skill_yel, size=8)  # throw 8 stones (the closer the score is to 1, the better)
        points_red.append(
            np.sum(Rs > np.max(Ys)))  # the reds get a point for each stone better than the opponent's best stone
        points_yel.append(
            np.sum(Ys > np.max(Rs)))  # the yels get a point for each stone better than the opponent's best stone

    return points_red, points_yel  # one team has zero, the other team <= 8


next_day = lambda day: (datetime.fromisoformat(day) + timedelta(days=1)).strftime(
    '%Y-%m-%d')  # example: next_day('2020-10-11') -> '2020-10-12'

next_year = lambda day: (datetime.fromisoformat(day) + timedelta(days=365)).strftime(
    '%Y-%m-%d')  # example: next_year('2020-10-11') -> '2021-10-11'

season_mark = lambda game_days: game_days[0].strftime('%y') + '/' + (game_days[0] + timedelta(days=365)).strftime(
    '%y')  # example return: '21/22'


def generate_game_days(starting_days,
                       matchweeks,
                       num_of_teams,
                       freq='7C',
                       possible_game_times=['22:00', '21:00', '20:00', '19:00', '18:00', '17:00']):
    num_of_games = np.ceil(num_of_teams / 2)
    game_index = num_of_games
    possible_game_times = possible_game_times.copy()
    days = []

    while game_index > 0:
        game_time = possible_game_times.pop()
        for starting_day in starting_days:
            days.append(pd.date_range(starting_day + ' ' + game_time, periods=matchweeks, freq=freq))
        game_index -= len(starting_days)

    while game_index < 0:
        days.pop()
        game_index += 1

    game_days = days[0]
    for specific_days in days:
        game_days = game_days.union(specific_days)

    return game_days


def simulate_season(team_codes, skill, matchweek='full_season', freq="7D", num_of_ends=8,
                    starting_days=['2020-10-11', '2020-10-12'], starting_id=0, seed=10):
    np.random.seed(seed)
    if matchweek == "full_season":
        matchweek = 2 * (len(team_codes) - 1)

    game_days = generate_game_days(starting_days, matchweek, len(team_codes), freq=freq)
    season = season_mark(game_days)

    matches = pd.DataFrame(index=range(len(game_days)), columns=["match_id",
                                                                 "season",
                                                                 "date",
                                                                 "matchweek",
                                                                 "red_team",
                                                                 "yellow_team",
                                                                 "hammer",
                                                                 "total_red",
                                                                 "total_yellow"])  # define dataframes

    ends = pd.DataFrame(index=range(len(game_days) * 8), columns=["match_id",
                                                                  "end",
                                                                  "points_red",
                                                                  "points_yellow"])  # define dataframes

    match_id = 0

    for week in range(matchweek):

        games = round_robin(team_codes, week)  # get pairings for current week
        for game in games:
            np.random.shuffle(game)  # random color selection
            red_pts, yellow_pts = simulate_match(skill[game[0]], skill[game[1]], ends=num_of_ends)  # match simulation

            matches.iloc[match_id] = pd.Series({"match_id": match_id + starting_id,
                                                "season": season,
                                                "date": game_days[match_id],
                                                "matchweek": week + 1,
                                                "red_team": game[0],
                                                "yellow_team": game[1],
                                                "hammer": np.random.choice(["red", "yellow"]),
                                                "total_red": int(np.nansum(red_pts)),  # important: nansum
                                                "total_yellow": int(np.nansum(yellow_pts))})  # important: nansum

            for end in range(num_of_ends):
                ends.iloc[num_of_ends * match_id + end] = pd.Series({"match_id": match_id + starting_id,
                                                                     "end": end + 1,
                                                                     "points_red": red_pts[end],
                                                                     "points_yellow": yellow_pts[end]})
            match_id += 1

    last_id = matches["match_id"].iloc[-1]
    ends = ends.astype({"match_id": "Int32"})
    ends = ends.astype({"end": "Int32"})
    return matches, ends, last_id


def simulate_tournament(skill, freq="7D", num_of_ends=8,
                        starting_days=['2020-12-07', '2020-12-08', '2020-12-09'], starting_id=0, seed=10):
    np.random.seed(seed)

    skill = list(skill.items())
    np.random.shuffle(skill)  # random pairings
    skill = dict(skill)
    games = np.split(np.array(list(skill.keys())), len(skill) // 2)

    game_days = generate_game_days(starting_days, 2, 16, freq=freq)
    season = season_mark(game_days)

    matches = pd.DataFrame(index=range(len(game_days) - 1), columns=["match_id",
                                                                     "season",
                                                                     "date",
                                                                     "matchweek",
                                                                     "red_team",
                                                                     "yellow_team",
                                                                     "hammer",
                                                                     "total_red",
                                                                     "total_yellow"])  # define dataframes

    ends = pd.DataFrame(index=range((len(game_days) - 1) * 8), columns=["match_id",
                                                                        "end",
                                                                        "points_red",
                                                                        "points_yellow"])  # define dataframes

    match_id = 0

    for stage in ["Round of 16", "Quater-finals", "Semi-finals", "Final"]:

        next_stage_games = []

        for i in range(len(games)):
            game = games.pop()
            np.random.shuffle(game)  # random color selection

            red_pts, yellow_pts = simulate_match(skill[game[0]], skill[game[1]], ends=num_of_ends)  # match simulation

            if red_pts > yellow_pts:
                next_stage_games.append(game[0])
            else:
                next_stage_games.append(game[1])

            matches.iloc[match_id] = pd.Series({"match_id": match_id + starting_id,
                                                "season": season,
                                                "date": game_days[match_id],
                                                "matchweek": (game_days.week - game_days.week[0] + 1)[match_id],
                                                "red_team": game[0],
                                                "yellow_team": game[1],
                                                "hammer": np.random.choice(["red", "yellow"]),
                                                "total_red": int(np.nansum(red_pts)),  # important: nansum
                                                "total_yellow": int(np.nansum(yellow_pts))})  # important: nansum

            for end in range(num_of_ends):
                ends.iloc[num_of_ends * match_id + end] = pd.Series({"match_id": match_id + starting_id,
                                                                     "end": end + 1,
                                                                     "points_red": red_pts[end],
                                                                     "points_yellow": yellow_pts[end]})
            match_id += 1

        if stage != "Final":
            games = np.split(np.array(next_stage_games), len(next_stage_games) // 2)

    last_id = matches["match_id"].iloc[-1]
    ends = ends.astype({"match_id": "Int32"})
    ends = ends.astype({"end": "Int32"})
    return matches, ends, last_id


def generate_PLPM_teams(players, num_of_mixed_doubles=20, num_of_CM_mixed_doubles=4, seed=10):
    np.random.seed(seed)
    players = players[players["retire_date"].isna()]
    players = players[["first_name", "last_name", "team_code"]]

    women = players[players["team_code"].isin(["CM AA", "CM BB"])]
    men = players[~players["team_code"].isin(["CM AA", "CM BB", "CM BS", "CM FP"])]

    men_PLPM = men.sample(num_of_CM_mixed_doubles).to_numpy()
    women_PLPM = women.sample(num_of_CM_mixed_doubles).to_numpy()

    # CM pairs

    CM_team_PLPM = list(zip(women_PLPM, men_PLPM))
    team_codes_PLPM = []
    team_names_PLPM = []

    for team in CM_team_PLPM:
        team_codes_PLPM.append("CM " + str(team[0][1])[:3] + "/" + str(team[1][1])[:3])
        team_names_PLPM.append("CM " + str(team[0][1]) + "/" + str(team[1][1]))

    # OTHER pairs

    num_of_other = num_of_mixed_doubles - num_of_CM_mixed_doubles
    other_women = np.random.choice(female_surnames, size=num_of_other)
    other_men = np.random.choice(male_surnames, size=num_of_other)
    other_clubs = np.random.choice(["KKC", "KS", "WKC", "WCC", "GCC", "CKS", "KCC"], size=num_of_other)
    other_teams_PLPM = list(zip(other_women, other_men))

    for index, team in enumerate(other_teams_PLPM):
        club = other_clubs[index]
        team_codes_PLPM.append(club + " " + team[0][:3] + "/" + team[1][:3])
        team_names_PLPM.append(club + " " + team[0] + "/" + team[1])

    teams_PLPM = pd.DataFrame({"team_code": team_codes_PLPM, "team_name": team_names_PLPM})
    return teams_PLPM


skill_PLM = assign_team_skill(team_codes_PLM, seed=SEED)
skill_PLK = assign_team_skill(team_codes_PLK, seed=SEED + 1)
skill_MPJ = assign_team_skill(team_codes_MPJ, seed=SEED + 2)


def clear_future_matches(matches_df, ends_df, stopdate):
    stop_id = matches_df[matches_df["date"] > stopdate]["match_id"].iloc[0]
    matches_df.loc[matches_df.date > stopdate, ['hammer', "total_red", "total_yellow"]] = np.nan
    ends_df.loc[ends_df.match_id >= stop_id, ['points_red', "points_yellow"]] = np.nan
    return matches_df, ends_df


def generate_PLM_matches_and_ends(SEED=10):
    (matches_20_21_PLM, ends_20_21_PLM, last_id) = simulate_season(team_codes_PLM,
                                                                   skill_PLM,
                                                                   starting_days=PLM_20_21_starting_days,
                                                                   seed=SEED + 3)

    (matches_21_22_PLM, ends_21_22_PLM, last_id) = simulate_season(team_codes_PLM,
                                                                   skill_PLM,
                                                                   starting_days=PLM_21_22_starting_days,
                                                                   starting_id=last_id + 1,
                                                                   seed=SEED + 4)

    matches_PLM = pd.concat([matches_20_21_PLM, matches_21_22_PLM]).reset_index(drop=True)
    ends_PLM = pd.concat([ends_20_21_PLM, ends_21_22_PLM]).reset_index(drop=True)
    matches_PLM, ends_PLM = clear_future_matches(matches_PLM, ends_PLM, stopdate)
    return matches_PLM, ends_PLM


def generate_PLK_matches_and_ends(SEED=10):
    (matches_20_21_PLK, ends_20_21_PLK, last_id) = simulate_season(team_codes_PLK,
                                                                   skill_PLK,
                                                                   starting_days=PLK_20_21_starting_days,
                                                                   seed=SEED + 5)

    (matches_21_22_PLK, ends_21_22_PLK, last_id) = simulate_season(team_codes_PLK,
                                                                   skill_PLK,
                                                                   starting_days=PLK_21_22_starting_days,
                                                                   starting_id=last_id + 1,
                                                                   seed=SEED + 6)

    matches_PLK = pd.concat([matches_20_21_PLK, matches_21_22_PLK]).reset_index(drop=True)
    ends_PLK = pd.concat([ends_20_21_PLK, ends_21_22_PLK]).reset_index(drop=True)
    return matches_PLK, ends_PLK


def generate_MPJ_matches_and_ends(SEED=10):
    (matches_20_21_MPJ, ends_20_21_MPJ, last_id) = simulate_tournament(skill_MPJ,
                                                                       starting_days=MPJ_20_21_starting_days,
                                                                       seed=SEED + 7)

    (matches_21_22_MPJ, ends_21_22_MPJ, last_id) = simulate_tournament(skill_MPJ,
                                                                       starting_id=last_id + 1,
                                                                       starting_days=MPJ_21_22_starting_days,
                                                                       seed=SEED + 8)

    matches_MPJ = pd.concat([matches_20_21_MPJ, matches_21_22_MPJ]).reset_index(drop=True)
    ends_MPJ = pd.concat([ends_20_21_MPJ, ends_21_22_MPJ]).reset_index(drop=True)
    return matches_MPJ, ends_MPJ


def generate_PLPM_matches_and_ends(teams_PLPM, SEED=10):
    team_codes_PLPM = teams_PLPM["team_code"].to_numpy()
    skill_PLPM = assign_team_skill(team_codes_PLPM)

    (matches_20_21_PLPM, ends_20_21_PLPM, last_id) = simulate_season(team_codes_PLPM,
                                                                     skill_PLPM,
                                                                     starting_days=PLPM_20_21_starting_days,
                                                                     seed=SEED + 9)

    (matches_21_22_PLPM, ends_21_22_PLPM, last_id) = simulate_season(team_codes_PLPM,
                                                                     skill_PLPM,
                                                                     starting_days=PLPM_21_22_starting_days,
                                                                     starting_id=last_id + 1,
                                                                     seed=SEED + 10)

    matches_PLPM = pd.concat([matches_20_21_PLPM, matches_21_22_PLPM]).reset_index(drop=True)
    ends_PLPM = pd.concat([ends_20_21_PLPM, ends_21_22_PLPM]).reset_index(drop=True)
    matches_PLPM, ends_PLPM = clear_future_matches(matches_PLPM, ends_PLPM, stopdate)
    return matches_PLPM, ends_PLPM


def all_matches_and_ends(teams_PLPM, SEED=10):
    matches_PLM, ends_PLM = generate_PLM_matches_and_ends(SEED=SEED)
    matches_PLK, ends_PLK = generate_PLK_matches_and_ends(SEED=SEED)
    matches_MPJ, ends_MPJ = generate_MPJ_matches_and_ends(SEED=SEED)
    matches_PLPM, ends_PLPM = generate_PLPM_matches_and_ends(teams_PLPM, SEED=SEED)

    matches_PLM["league_code"] = "PLM"
    matches_PLK["league_code"] = "PLK"
    matches_MPJ["league_code"] = "MPJ"
    matches_PLPM["league_code"] = "PLPM"

    all_matches = matches_PLM.append([matches_PLK, matches_MPJ, matches_PLPM])
    all_matches.reset_index(drop=True, inplace=True)
    all_matches = all_matches[["match_id",
                               "date",
                               "season",
                               "league_code",
                               "matchweek",
                               "red_team",
                               "yellow_team",
                               "hammer",
                               "total_red",
                               "total_yellow"]]

    all_matches["temporary_index"] = range(len(all_matches))

    all_ends = ends_PLM.append([ends_PLK, ends_MPJ, ends_PLPM])
    all_ends["temporary_index"] = np.repeat(range(len(all_matches)), 8)
    matches_and_ends = all_ends.join(all_matches, on="temporary_index", lsuffix="|ends", rsuffix="|matches")
    matches_and_ends = matches_and_ends.sort_values(by=["date", "end"])
    all_matches = matches_and_ends[["match_id|matches",
                                    "date",
                                    "season",
                                    "league_code",
                                    "matchweek",
                                    "red_team",
                                    "yellow_team",
                                    "hammer",
                                    "total_red",
                                    "total_yellow"]].drop_duplicates()

    all_matches = all_matches.rename(columns={"match_id|matches": "match_id"})
    all_matches["match_id"] = range(len(all_matches))
    all_ends = matches_and_ends[["match_id|ends",
                                 "end",
                                 "points_red",
                                 "points_yellow"]]

    all_ends = all_ends.rename(columns={"match_id|ends": "match_id"})
    all_ends["match_id"] = np.repeat(range(len(all_matches)), 8)

    return all_matches, all_ends


def generate_all_teams(teams_PLPM, SEED=10):
    np.random.seed(SEED)
    team_codes_PLPM = teams_PLPM["team_code"].to_numpy()

    teams_PLM["league_code"] = "PLM"
    teams_PLK["league_code"] = "PLK"
    teams_MPJ["league_code"] = "MPJ"
    teams_PLPM["league_code"] = "PLPM"

    all_teams = teams_PLM.append([teams_PLK, teams_MPJ, teams_PLPM])

    established = []
    for code in all_teams["team_code"]:
        if code in all_team_codes:  # primary CM teams
            established.append(establishment_dates[code])
        elif code.startswith("CM"):  # CM mixed doubles
            established.append(starting_season - timedelta(np.random.randint(10, 60)))
        else:  # not CM teams
            established.append(random_date(date_fromiso("2000-01-01"), date_fromiso("2020-01-01")))

    all_teams["established"] = established

    all_teams.to_csv(os.path.join("csv", "teams.csv"), index=False)
    return all_teams

import numpy as np
from data.data import *
from statistics import stdev
import pandas as pd
import json

def simulation(N= 10000, ff_data = ff_data, weights= weights, match_ups = match_ups):
    print('Prepping Data for Simulations')
    for team in ff_data:
        weighted_weekly = sum([weight*score for weight,score in zip(weights, ff_data[team]['scores'])])
        ff_data[team]['weighted_avg'] = (weighted_weekly*(.67))+(ff_data[team]['exp_week_points']*(.33))
        ff_data[team]['std'] = stdev(ff_data[team]['scores'])
        ff_data[team]['total_points'] = sum(ff_data[team]['scores'])
        ff_data[team]['sim_wins'] = []
        ff_data[team]['sim_seed'] = []
        ff_data[team]['sim_points'] = []
        ff_data[team]['sim_mp'] = []
        ff_data[team]['sim_first'] = []

    for n in range(N):
        def _seed(ff_data , n):
            teams = []
            sim_total_points = []
            sim_total_wins = []
            for team in ff_data:
                teams.append(team)
                sim_total_points.append(ff_data[team]['total_points'] + ff_data[team]['sim_points'][n])
                sim_total_wins.append(ff_data[team]['current_wins'] + ff_data[team]['sim_wins'][n])
            temp_df = pd.DataFrame(list(zip(teams, sim_total_points, sim_total_wins)),
                                 columns = ['team', 'sim_total_points', 'sim_total_wins'])
            temp_df['seed'] = temp_df.sort_values(by=['sim_total_wins', 'sim_total_points'], ascending=False)\
                                     .reset_index()\
                                     .sort_values('index')\
                                     .index + 1
            temp_df.set_index('team', inplace=True)
            return temp_df




        for home in match_ups:
            away = match_ups[home]
            home_pts = np.random.normal(loc = ff_data[home]['weighted_avg'],
                                        scale = ff_data[home]['std'],
                                        size = 1)
            away_pts = np.random.normal(loc = ff_data[away]['weighted_avg'],
                                        scale = ff_data[away]['std'],
                                        size = 1)

            if home_pts > away_pts:
                ff_data[home]['sim_wins'].append(1)
                ff_data[away]['sim_wins'].append(0)
            elif home_pts == away_pts:
                ff_data[home]['sim_wins'].append(0)
                ff_data[away]['sim_wins'].append(0)
            else:
                ff_data[home]['sim_wins'].append(0)
                ff_data[away]['sim_wins'].append(1)

            ff_data[home]['sim_points'].append(home_pts[0])
            ff_data[away]['sim_points'].append(away_pts[0])
        seeds_df = _seed(ff_data = ff_data, n = n)

        for team in ff_data:
            seed = seeds_df.loc[team]['seed']
            ff_data[team]['sim_seed'].append(seed)
            if seed <= 6:
                ff_data[team]['sim_mp'].append(1)
            if seed == 1:
                ff_data[team]['sim_first'].append(1)
    final_teams = []
    final_pct_win = []
    final_pct_mp = []
    final_pct_first = []
    final_avg_seed = []
    final_pct_sec = []
    final_pct_third = []
    final_pct_fourth = []
    final_pct_fifth = []
    final_pct_sixth =[]
    for team in ff_data:
        final_teams.append(team)
        final_pct_win.append(round((sum(ff_data[team]['sim_wins'])/N), 2))
        final_pct_mp.append(round((sum(ff_data[team]['sim_mp'])/N),2))
        final_pct_first.append(round((sum(ff_data[team]['sim_first']) / N),2))
        final_avg_seed.append(round((sum(ff_data[team]['sim_seed']) / N),2))
        times = []
        for s in range(2,7):
            times.append(round(len([seed for seed in ff_data[team]['sim_seed'] if seed == s])/N,2))
        final_pct_sec.append(times[0])
        final_pct_third.append(times[1])
        final_pct_fourth.append(times[2])
        final_pct_fifth.append(times[3])
        final_pct_sixth.append(times[4])

    final_df = pd.DataFrame(list(zip(final_teams,
                                     final_pct_win,
                                     final_pct_mp,
                                     final_pct_first,
                                     final_pct_sec,
                                     final_pct_third,
                                     final_pct_fourth,
                                     final_pct_fifth,
                                     final_pct_sixth,
                                     final_avg_seed)),
                            columns = ['team',
                                       'pct_win_week',
                                       'pct_make_playoffs',
                                       'pct_first',
                                       'pct_sec',
                                       'pct_third',
                                       'pct_fourth',
                                       'pct_fifth',
                                       'pct_sixth',
                                       'avg_seed'])

    return final_df, ff_data



analysis_df, ff_data_analysis = simulation(N=10000)

print(analysis_df)
analysis_df.to_csv('./data/simulation_df.csv')

with open('./data/ff_data.json', 'w') as l:
    json.dump(ff_data_analysis, l)




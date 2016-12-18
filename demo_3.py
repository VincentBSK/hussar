__author__ = 'BSK'
import matplotlib.pyplot as plt
import numpy as np
import os

from analyzers import MatchAnalyzer
from sklearn import linear_model

ft_goal_list = []
players_dict = {}
teams_dict = {}

def generate_ft_goal_data_from_list(temp_game,goal_list):
    teams = [temp_game.home_id,temp_game.away_id]
    current_goals = [0,0]
    goals = []

    # last_time = temp_game.new_events[-1].minsec
    # print last_time
    for goal_event in goal_list:
        if goal_event.minsec >= 5399:
            print temp_ma.game_id + ',' + str(goal_event.minsec) + ',' + str(goal_event.player_id) + ',' + players_dict[goal_event.player_id].name
            if goal_event.team_id == teams[0]:
                goals.append((goal_event,temp_game.game_id,current_goals[0],current_goals[1]))
            else:
                goals.append((goal_event,temp_game.game_id,current_goals[1],current_goals[0]))
        if goal_event.team_id == teams[0]:
            current_goals[0] += 1
        else:
            current_goals[1] += 1

    return goals

ft_goals = []

dir_list = ['EC2013','EC2014','EC2015','EC2016','DL2013','DL2014','DL2015','DL2016','EPL2013','EPL2014','EPL2015','EPL2016','LL2013','LL2014','LL2015','LL2016']
#dir_list = ['EC2013']
for temp_dir in dir_list:
    match_files = os.listdir('match_results/' + temp_dir + '/')
    for match_file in match_files:
        if match_file[0] == '.':
            continue
        temp_ma = MatchAnalyzer('match_results/' + temp_dir + '/' + match_file)

        for pa in temp_ma.players:
            if pa.player_id not in players_dict.keys():
                players_dict[pa.player_id] = pa

        for t in temp_ma.teams:
            if t.team_id not in teams_dict.keys():
                teams_dict[t.team_id] = t

        goal_list = []
        for temp_event in temp_ma.new_events:
            if temp_event.type == 1 and temp_event.result == 1:
                goal_list.append(temp_event)
            if temp_event.type == 1 and temp_event.result == 1 and temp_event.minsec >= 5400:
                ft_goal_list.append(temp_event)

        print temp_ma.game_id
        temp_ft_goals = generate_ft_goal_data_from_list(temp_ma,goal_list)
        ft_goals.extend(temp_ft_goals)
        if len(temp_ft_goals) > 1:
            print 'fuck!!! ' +  str(temp_ft_goals[0][1])

fk_ft_goals = []
for ft_goal in ft_goals:
    if ft_goal[2] == ft_goal[3] or ft_goal[2] == ft_goal[3] - 1:
        fk_ft_goals.append(ft_goal)
print len(ft_goals)
print len(fk_ft_goals)

ft_player_table = {}
ft_team_table = {}
ft_oteam_table = {}
for fk_ft_goal in fk_ft_goals:
    if fk_ft_goal[0].player_id not in ft_player_table.keys():
        ft_player_table[fk_ft_goal[0].player_id] = [fk_ft_goal]
    else:
        ft_player_table[fk_ft_goal[0].player_id].append(fk_ft_goal)

    if fk_ft_goal[0].team_id not in ft_team_table.keys():
        ft_team_table[fk_ft_goal[0].team_id] = [fk_ft_goal]
    else:
        ft_team_table[fk_ft_goal[0].team_id].append(fk_ft_goal)

    if fk_ft_goal[0].other_team_id not in ft_oteam_table.keys():
        ft_oteam_table[fk_ft_goal[0].other_team_id] = [fk_ft_goal]
    else:
        ft_oteam_table[fk_ft_goal[0].other_team_id].append(fk_ft_goal)

for key in ft_player_table.keys():
    print str(key) + ',' + players_dict[key].name + ',' + str(len(ft_player_table[key]))

for key in ft_team_table.keys():
    print str(key) + ',' + teams_dict[key].name + ',' + str(len(ft_team_table[key]))

print 'OTEAMS:'

for key in ft_oteam_table.keys():
    print str(key) + ',' + teams_dict[key].name + ',' + str(len(ft_oteam_table[key]))
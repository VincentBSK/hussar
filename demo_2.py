__author__ = 'BSK'
import matplotlib.pyplot as plt
import numpy as np
import os

from analyzers import MatchAnalyzer
from sklearn import linear_model

match_files = os.listdir('match_results/LL2015/')

teams = []
all_goal_recorders = []
all_goal_recorders_oppo = []

class GoalRecorder:
    def __init__(self,game_id,goals):
        self.game_id = game_id
        self.goals = goals

def generate_goal_data_from_list(teams,goal_list):
    current_goals = [0,0]
    goals = {teams[0]:[],teams[1]:[]}
    for goal_event in goal_list:
        if goal_event.team_id == teams[0]:
            current_goals[0] += 1
        else:
            current_goals[1] += 1


for match_file in match_files:
    if match_file[0] == '.':
        continue
    temp_ma = MatchAnalyzer('match_results/LL2015/' + match_file)

    goal_list = []
    for temp_event in temp_ma.events:
        if temp_event.type == 1 and temp_event.result == 0:
            goal_list.append(temp_event)
    generate_goal_data_from_list([temp_ma.home_id,temp_ma.away_id],goal_list)

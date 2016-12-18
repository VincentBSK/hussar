__author__ = 'BSK'
import matplotlib.pyplot as plt
import numpy as np
import os

from analyzers import MatchAnalyzer
from sklearn import linear_model

match_files = os.listdir('match_results/LL2015/')
players_dict = {}
teams_dict = {}
stat_dicts = []
team_stat_dicts = []
team_stat_dicts_success = []

xy_data = []
z_data = []

for _ in xrange(6):
    stat_dicts.append({})
    team_stat_dicts.append({})
    team_stat_dicts_success.append({})

result_temps = [0,0,0,1,1,1]
for match_file in match_files:
    if match_file[0] == '.':
        continue
    temp_ma = MatchAnalyzer('match_results/LL2015/' + match_file)
    # for pa in temp_ma.players:
    #     if pa.player_id not in players_dict.keys():
    #         players_dict[pa.player_id] = pa

    active_ids = temp_ma.active_player_ids()
    for pa in temp_ma.players:
        if pa.player_id in active_ids and pa.state == 'playing' and pa.player_id not in players_dict.keys():
            players_dict[pa.player_id] = pa

    for t in temp_ma.teams:
        if t.team_id not in teams_dict.keys():
            teams_dict[t.team_id] = t

    temp_stat_dict_0 = temp_ma.team_stat(0,0)
    temp_stat_dict_1 = temp_ma.team_stat(1,1)
    ps = [0,0]
    gs = [0,0]
    ts = ['','']
    for i in xrange(len(temp_stat_dict_0.keys())):
        key = temp_stat_dict_0.keys()[i]
        ts[i] = key[1]
        ps[i] = int(temp_stat_dict_0[key])
        if key in temp_stat_dict_1.keys():
            gs[i] = temp_stat_dict_1[key]

    # xy_data.append([ps[0],gs[0] - gs[1]])
    # xy_data.append([ps[1],gs[1] - gs[0]])
    xy_data.append([ps[0],gs[0]])
    xy_data.append([ps[1],gs[1]])
    if gs[1] == 0 or gs[0] == 0:
        print temp_ma.game_id
    z_data.append(ts[0])
    z_data.append(ts[1])

    xy = np.array(xy_data)
    x = xy[:,0]
    # if xy.shape[0] > 10:
    #     regr = linear_model.LinearRegression()
    #     regr.fit(x[:,None].astype(np.float), xy[:,1].astype(np.float))
    #
    #     y_true = xy[:,1].astype(np.float)
    #     y_true_mean = np.mean(y_true)
    #     y_pred = regr.predict(x[:,None].astype(np.float))
    #     SSReg = np.sum((y_pred - y_true_mean) ** 2)
    #     RSS = np.sum((y_pred - y_true) ** 2)
    #     MS = RSS / (xy.shape[0] - 2)
    #     R_2 = SSReg / np.sum((y_true - y_true_mean) ** 2)
    #     F = SSReg / MS
    #     equal_str = 'goal_attempts = ' + str(regr.coef_[0])[:6] + ' * passes + ' + str(regr.intercept_)[:4] + '    R^2 = ' + str(R_2)[:5] + '    F = ' + str(F)[:5]
    #
    #     f = plt.figure(figsize=(10, 10))
    #     plt.xticks(fontsize=20)
    #     plt.yticks(fontsize=20)
    #     ax = plt.subplot(aspect='equal')
    #     plt.ylim(0,40)
    #     plt.xlim(150,800)
    #     plt.xlabel('passes',fontsize=20)
    #     plt.ylabel('goal_attempts',fontsize=20)
    #     plt.xticks(fontsize=20)
    #     plt.yticks(fontsize=20)
    #     ax.set_aspect(1./ax.get_data_ratio())
    #     sc = ax.scatter(xy[:,0], xy[:,1], lw=0, s=50)
    #     xx = np.linspace(150, 800, 10)
    #     yy = regr.predict(xx[:,None])
    #     ax.plot(xx, yy, 'r-', linewidth = 2)
    #     plt.text(500,35,equal_str,color='black',ha='center',fontsize=20)
    #     plt.show()

    for i in xrange(6):
        temp_stat_dict = temp_ma.player_stat(i,result_temps[i])
        stat_dicts[i].update(temp_stat_dict)
        temp_stat_dict = temp_ma.team_stat(i,0)
        team_stat_dicts[i].update(temp_stat_dict)
        temp_stat_dict = temp_ma.team_stat(i,1)
        team_stat_dicts_success[i].update(temp_stat_dict)

    print match_file

x = xy[:,0]
regr = linear_model.LinearRegression()
regr.fit(x[:,None].astype(np.float), xy[:,1].astype(np.float))

y_true = xy[:,1].astype(np.float)
y_true_mean = np.mean(y_true)
y_pred = regr.predict(x[:,None].astype(np.float))
SSReg = np.sum((y_pred - y_true_mean) ** 2)
RSS = np.sum((y_pred - y_true) ** 2)
MS = RSS / (xy.shape[0] - 2)
R_2 = SSReg / np.sum((y_true - y_true_mean) ** 2)
F = SSReg / MS
equal_str = 'goal_attempts = ' + str(regr.coef_[0])[:6] + ' * passes + ' + str(regr.intercept_)[:4] + '    R^2 = ' + str(R_2)[:5] + '    F = ' + str(F)[:5]

f = plt.figure(figsize=(10, 10))
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax = plt.subplot(aspect='equal')
plt.ylim(0,40)
plt.xlim(150,800)
plt.xlabel('passes',fontsize=20)
plt.ylabel('goal_attempts',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_aspect(1./ax.get_data_ratio())
sc = ax.scatter(xy[:,0], xy[:,1], lw=0, s=50)
xx = np.linspace(150, 800, 10)
yy = regr.predict(xx[:,None])
ax.plot(xx, yy, 'r-', linewidth = 2)
plt.text(500,35,equal_str,color='black',ha='center',fontsize=20)
plt.show()

team_stat_dict = {}
team_stat_dict_success = {}
for i in xrange(2):
    team_stat_dict = {}
    team_stat_dict_success = {}
    for key in team_stat_dicts[i].keys():
        if key[1] not in team_stat_dict.keys():
            team_stat_dict[key[1]] = team_stat_dicts[i][key]
        else:
            team_stat_dict[key[1]] += team_stat_dicts[i][key]

    for key in team_stat_dicts_success[i].keys():
        if key[1] not in team_stat_dict_success.keys():
            team_stat_dict_success[key[1]] = team_stat_dicts_success[i][key]
        else:
            team_stat_dict_success[key[1]] += team_stat_dicts_success[i][key]

    for key in team_stat_dict.keys():
        print teams_dict[key].name,team_stat_dict[key] / 38.0,team_stat_dict_success[key] / 38.0, float(team_stat_dict_success[key])/float(team_stat_dict[key])

for i in xrange(6):
    temp_stat_dict = stat_dicts[i]
    max_key = temp_stat_dict.keys()[0]
    max_value = 0
    for key in temp_stat_dict.keys():
        if int(temp_stat_dict[key]) > int(max_value):
            max_key = key
            max_value = int(temp_stat_dict[key])
    for key in temp_stat_dict.keys():
        if int(temp_stat_dict[key]) == int(max_value):
            print (i,key[0],key[1],players_dict[key[1]].name,max_value)
    # print (i,max_key[0],max_key[1],players_dict[max_key[1]].name,max_value)

min_key = players_dict.keys()[0]
min_str = '99999999'
for key in players_dict.keys():
    if int(players_dict[key].born_day) < int(min_str) and players_dict[key].born_day != '00000000':
        min_key = key
        min_str = players_dict[key].born_day

max_key = players_dict.keys()[0]
max_str = '00000000'
for key in players_dict.keys():
    if int(players_dict[key].born_day) > int(max_str) and players_dict[key].born_day != '00000000':
        max_key = key
        max_str = players_dict[key].born_day

print players_dict[min_key].name
print players_dict[min_key].born_day

print players_dict[max_key].name
print players_dict[max_key].born_day

a = 1




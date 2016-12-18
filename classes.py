__author__ = 'asus'

# type:
# pass = 0
# goal_attempt = 1
#

event_prior = [0,2,1,3,4,5]
def cmp_event(a,b):
    if a.minsec < b.minsec:
        return -1
    elif a.minsec > b.minsec:
        return 1
    else:
        if event_prior[a.type] < event_prior[b.type]:
            return  -1
        elif event_prior[a.type] > event_prior[b.type]:
            return 1
        else:
            return 0

class Event:
    def __init__(self,type,main_type,minsec,team_id,player_id,result,start_p,if_it,attribs = [],end_p = (),other_team_id = '-1',other_player_id = -1):
        self.type = type
        self.main_typ = main_type
        self.minsec = minsec
        self.team_id = team_id
        self.player_id = player_id
        self.result = result
        self.start_p = start_p
        self.if_it = if_it
        self.attribs = attribs
        self.end_p = end_p
        self.other_team_id = other_team_id
        self.other_player_id = other_player_id

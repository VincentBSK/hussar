__author__ = 'asus'
from xml.etree import ElementTree
from classes import Event,cmp_event



class PlayerAnalyzer:
    def __init__(self,root):
        self.root = root
        self.player_id = root.attrib['id']
        self.name = root.find('name').text
        dob_strs = root.find('dob').text.split('/')
        self.state = root.find('state').text
        self.born_day = dob_strs[2] + dob_strs[1] + dob_strs[0]

class TeamAnalyzer:
    def __init__(self,root):
        self.team_id = root.attrib['id']
        self.name = root.find('short_name').text



class MatchAnalyzer:
    def __init__(self,file):
        self.game_id = file.split('/')[-1].split('.')[0]

        root = ElementTree.parse(file).getroot()

        self.teams = []
        temp_node = root[0].find('game')
        for team in temp_node.findall('team'):
            self.teams.append(TeamAnalyzer(team))
            if team.find('state').text == 'home':
                self.home_id = team.attrib['id']
            else:
                self.away_id = team.attrib['id']

        self.players = []
        players_node = root[0].find('players')
        for player_node in players_node:
            self.players.append(PlayerAnalyzer(player_node))

        filter_node = root[0].find('filters')
        self.events = []

        time_nodes = filter_node.find('all_passes').findall('time_slice')
        for time_node in time_nodes:
            event_nodes = time_node.findall('event')
            for event_node in event_nodes:
                player_id = event_node.attrib['player_id']
                team_id = event_node.attrib['team_id']
                minsec = int(event_node.attrib['minsec'])
                if_it = 0
                if 'injurytime_play' in event_node.attrib.keys():
                    if int(event_node.attrib['injurytime_play']) > 0:
                        if_it = 1
                # if minsec > 5400 or (minsec > 2700 and if_it == 0):
                #     minsec += 10000

                if event_node.attrib['type'] == 'completed':
                    result = 1
                else:
                    result = 0
                tokens = event_node.find('start').text.split(',')
                start_p = (float(tokens[0]),float(tokens[1]))
                tokens = event_node.find('end').text.split(',')
                try:
                    end_p = (float(tokens[0]),float(tokens[1]))
                except:
                    end_p = ()
                attribs = []
                if event_node.find('long_ball') != None:
                    attribs.append('long_ball')
                if event_node.find('headed') != None:
                    attribs.append('headed')
                if event_node.find('through_ball') != None:
                    attribs.append('through_ball')
                if 'k' in event_node.attrib.keys():
                    attribs.append('key_pass')
                if 'a' in event_node.attrib.keys():
                    attribs.append('assist')

                self.events.append(Event(0,0,minsec,team_id,player_id,result,start_p,if_it,attribs,end_p=end_p))

        time_nodes = filter_node.find('goals_attempts').findall('time_slice')
        for time_node in time_nodes:
            event_nodes = time_node.findall('event')
            for event_node in event_nodes:
                player_id = event_node.attrib['player_id']
                team_id = event_node.attrib['team_id']

                if team_id == self.home_id:
                    other_team_id = self.away_id
                else:
                    other_team_id = self.home_id

                if 'minsec' in event_node.attrib.keys():
                    minsec = int(event_node.attrib['minsec'])
                else:
                    mins = int(event_node.attrib['mins'])
                    secs = int(event_node.attrib['secs'])
                    minsec = mins * 60 + secs
                if_it = 0
                if 'injurytime_play' in event_node.attrib.keys():
                    if int(event_node.attrib['injurytime_play']) > 0:
                        if_it = 1
                # if minsec > 5400 or (minsec > 2700 and if_it == 0):
                #     minsec += 10000

                if event_node.attrib['type'] == 'goal':
                    result = 1
                else:
                    result = 0
                child_node = event_node.find('start')
                if child_node.text != None:
                    tokens = child_node.text.split(',')
                    start_p = (float(tokens[0]),float(tokens[1]))
                else:
                    continue
                child_node = event_node.find('end')
                tokens = child_node.text.split(',')
                end_p = (float(tokens[0]),float(tokens[1]))
                attribs = [type]

                self.events.append(Event(1,0,minsec,team_id,player_id,result,start_p,if_it,attribs,end_p=end_p,other_team_id=other_team_id))

        time_nodes = filter_node.find('takeons').findall('time_slice')
        for time_node in time_nodes:
            event_nodes = time_node.findall('event')
            for event_node in event_nodes:
                player_id = event_node.attrib['player_id']
                team_id = event_node.find('team_id').text
                if 'minsec' in event_node.attrib.keys():
                    minsec = int(event_node.attrib['minsec'])
                else:
                    mins = int(event_node.attrib['mins'])
                    secs = int(event_node.attrib['secs'])
                    minsec = mins * 60 + secs
                if_it = 0
                if 'injurytime_play' in event_node.attrib.keys():
                    if int(event_node.attrib['injurytime_play']) > 0:
                        if_it = 1
                # if minsec > 5400 or (minsec > 2700 and if_it == 0):
                #     minsec += 10000

                if event_node.attrib['type'] == 'Success':
                    result = 1
                else:
                    result = 0

                tokens = event_node.find('loc').text.split(',')
                start_p = (float(tokens[0]),float(tokens[1]))
                if 'other_team' in event_node.attrib.keys():
                    other_team_id = event_node.attrib['other_team']
                else:
                    other_team_id = '0'
                if 'other_player' in event_node.attrib.keys():
                    other_player_id = event_node.attrib['other_player']
                else:
                    other_player_id = '0'
                attribs = []

                self.events.append(Event(2,0,minsec,team_id,player_id,result,start_p,if_it,attribs,other_team_id=other_team_id,other_player_id=other_player_id))

        time_nodes = filter_node.find('interceptions').findall('time_slice')
        for time_node in time_nodes:
            event_nodes = time_node.findall('event')
            for event_node in event_nodes:
                player_id = event_node.attrib['player_id']
                team_id = event_node.attrib['team_id']
                if 'minsec' in event_node.attrib.keys():
                    minsec = int(event_node.attrib['minsec'])
                else:
                    mins = int(event_node.attrib['mins'])
                    secs = int(event_node.attrib['secs'])
                    minsec = mins * 60 + secs
                if_it = 0
                if 'injurytime_play' in event_node.attrib.keys():
                    if int(event_node.attrib['injurytime_play']) > 0:
                        if_it = 1
                # if minsec > 5400 or (minsec > 2700 and if_it == 0):
                #     minsec += 10000

                result = 1

                child_node = event_node.find('loc')
                tokens = child_node.text.split(',')
                start_p = (float(tokens[0]),float(tokens[1]))

                attribs = []
                if event_node.find('headed') != None:
                    if event_node.find('headed').text == 'true':
                        attribs.append('headed')

                self.events.append(Event(3,1,minsec,team_id,player_id,result,start_p,if_it,attribs))

        time_nodes = filter_node.find('clearances').findall('time_slice')
        for time_node in time_nodes:
            event_nodes = time_node.findall('event')
            for event_node in event_nodes:
                player_id = event_node.attrib['player_id']
                team_id = event_node.attrib['team_id']
                if 'minsec' in event_node.attrib.keys():
                    minsec = int(event_node.attrib['minsec'])
                else:
                    mins = int(event_node.attrib['mins'])
                    secs = int(event_node.attrib['secs'])
                    minsec = mins * 60 + secs
                if_it = 0
                if 'injurytime_play' in event_node.attrib.keys():
                    if int(event_node.attrib['injurytime_play']) > 0:
                        if_it = 1
                # if minsec > 5400 or (minsec > 2700 and if_it == 0):
                #     minsec += 10000

                if event_node.attrib['type'] == 'failed':
                    result = 0
                else:
                    result = 1

                child_node = event_node.find('loc')
                tokens = child_node.text.split(',')
                start_p = (float(tokens[0]),float(tokens[1]))

                attribs = []
                if event_node.find('headed') != None:
                    if event_node.find('headed').text == 'true':
                        attribs.append('headed')

                self.events.append(Event(4,1,minsec,team_id,player_id,result,start_p,if_it,attribs))

        time_nodes = filter_node.find('tackles').findall('time_slice')
        for time_node in time_nodes:
            event_nodes = time_node.findall('event')
            for event_node in event_nodes:
                other_player_id = event_node.attrib['player_id']
                other_team_id = event_node.attrib['team']
                if 'minsec' in event_node.attrib.keys():
                    minsec = int(event_node.attrib['minsec'])
                else:
                    mins = int(event_node.attrib['mins'])
                    secs = int(event_node.attrib['secs'])
                    minsec = mins * 60 + secs
                if_it = 0
                if 'injurytime_play' in event_node.attrib.keys():
                    if int(event_node.attrib['injurytime_play']) > 0:
                        if_it = 1
                # if minsec > 5400 or (minsec > 2700 and if_it == 0):
                #     minsec += 10000

                if event_node.attrib['type'] == 'Success':
                    result = 1
                else:
                    result = 0

                tokens = event_node.find('loc').text.split(',')
                start_p = (float(tokens[0]),float(tokens[1]))
                team_id = event_node.find('tackler_team').text
                player_id = event_node.find('tackler').text
                attribs = []
                if type == 'Fouled':
                    attribs.append('fouled')

                self.events.append(Event(5,1,minsec,team_id,player_id,result,start_p,if_it,attribs,other_team_id=other_team_id,other_player_id=other_player_id))
        self.new_events = sorted(self.events,cmp=cmp_event)
        a = 1

    def active_player_ids(self):
        active_player_ids = []
        for event in self.events:
            if event.player_id not in active_player_ids:
                active_player_ids.append(event.player_id)
        return active_player_ids

    def team_stat(self,event_type,result_template = 0):
        stat_dict = {}
        for event in self.events:
            if event.type == event_type and event.result >= result_template:
                if (self.game_id,event.team_id) not in stat_dict.keys():
                    stat_dict[(self.game_id,event.team_id)] = 1
                else:
                    stat_dict[(self.game_id,event.team_id)] += 1
        return stat_dict

    def player_stat(self,event_type,result_template = 0):
        stat_dict = {}
        for event in self.events:
            if event.type == event_type and event.result >= result_template:
                if (self.game_id,event.player_id) not in stat_dict.keys():
                    stat_dict[(self.game_id,event.player_id)] = 1
                else:
                    stat_dict[(self.game_id,event.player_id)] += 1

        return stat_dict



if __name__ == '__main__':
    ma = MatchAnalyzer('match_results/DL2015/14975.xml')



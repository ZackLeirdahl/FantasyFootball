import json, os
from yahoo_oauth import OAuth2
from endpoints import *

class YahooFantasyAPI:
    def __init__(self):
        self.session = self.get_session()
        self.fmt = 'json'

    def get_session(self):
        oauth = OAuth2(None,None,from_file= 'fantasy_app\\static\\auth\\oauth2.json')
        if not oauth.token_is_valid():
            oauth.refresh_access_token()
        return oauth.session

    def session_request(self, url):
        data = self.session.get(url, params={'format':self.fmt})
        return json.loads(data.text)
        
    def get_user_data(self, details = {}):
        data = self.session_request(league_standings())['fantasy_content']['league'][1]['standings'][0]['teams']
        for k in list(data.keys())[:-1]:
            team_id = data[k]['team'][0][1]['team_id']
            details[team_id] = {}
            t = data[k]['team'][0]
            for li in [0,1,2,5,7,9,10,18]:
                if li == 0:
                    details[team_id]['team_key'] = t[li]['team_key']
                elif li == 1:
                    details[team_id]['team_id'] = t[li]['team_id']
                elif li == 5:
                    details[team_id]['image'] = data[k]['team'][0][5]['team_logos'][0]['team_logo']['url']
                elif li == 7:
                    details[team_id]['waiver_priority'] = t[li]['waiver_priority']
                elif li == 9:
                    details[team_id]['number_of_moves'] = t[li]['number_of_moves']
                elif li == 10:
                    details[team_id]['number_of_trades'] = t[li]['number_of_trades']
                elif li == 18:
                    manager = data[k]['team'][0][-1]['managers'][0]['manager']
                    details[team_id]['manager_id'] = manager['manager_id']
                    details[team_id]['nickname'] = manager['nickname']
                    try:
                        details[team_id]['email'] = manager['email']
                    except:
                        continue
                else:
                    details[team_id]['name'] = t[li]['name']
        return details
    
    def get_matchup_data(self, team_id, week, details = {}):
        data = self.session_request(team_matchups(team_id, week))['fantasy_content']['team'][1]['matchups']['0']['matchup']
        for k, v in data.items():
            if k in ['week', 'week_start', 'week_end', 'status', 'is_playoffs', 'is_consolation', 'is_matchup_recap_available']:
                details[k] = v
        matchup_key = details['week']
        for i in range(2):
            branch = data['0']['teams'][str(i)]['team']
            team_id = branch[0][1]['team_id']
            matchup_key += '-' + team_id
            details[team_id] = {}
            for k, v in branch[1].items():
                if k in ['team_points', 'team_projected_points']:
                    details[team_id][k]= v['total']
                else:
                    details[team_id][k] = v
        matchup_key += '-' + details['week_start'][:4]
        return [matchup_key, details]       
        
    def get_player_stats(self, player_id = '29396'):
        stats = {player_id: {}}
        for stat in self.session_request(players_stats_by_key([player_id]))['fantasy_content']['players']['0']['player'][1]['player_stats']['stats']:
            stat = stat['stat']
            stat_id = stat['stat_id']
            stats[player_id][stat_id] = {'value':stat['value']}
        return stats

    def get_standings(self, standings = {}):
        data = self.session_request(league_standings())['fantasy_content']['league'][1]['standings'][0]['teams']
        for k, v in data.items():
            if k != 'count':
                team_id = data[k]['team'][0][1]['team_id']
                standings[team_id] = data[k]['team'][-1]['team_standings']['outcome_totals']
                standings[team_id].update({'rank': data[k]['team'][-1]['team_standings']['rank'], 'points_for': data[k]['team'][-1]['team_standings']['points_for'], 'points_against': data[k]['team'][-1]['team_standings']['points_against']})
        return standings

    def get_team_roster(self, team_id = '1'):
        data = self.session_request(team_roster(team_id))['fantasy_content']['team'][1]['roster']['0']
        print(data)
    
    def get_player_description(self, player_ids = None, players = {}):
        if type(player_ids) == str:
            data = self.session_request(players_by_key([player_ids]))
        else:
            data = self.session_request(players_by_key(player_ids))
        data = data['fantasy_content']['players']
        for k, v in data.items():
            if type(v) == dict:
                branch = v['player'][0]
                player_id = branch[1]['player_id']
                players[player_id] = {}
                for i in range(len(branch)):
                    attr = branch[i]
                    if type(attr) == dict:
                        for kk, vv in attr.items():
                            if kk in ['player_id', 'name', 'editorial_team_key','editorial_team_full_name','editorial_team_abbr', 'display_position']:
                                if kk != 'name':
                                    players[player_id][kk] = vv
                                else:
                                    players[player_id]['first_name'] = vv['first']
                                    players[player_id]['last_name'] = vv['last']
        return players

    def get_stat_categories(self, stats = {}):
        modifiers = {stat['stat']['stat_id'] : {'value': float(stat['stat']['value'])} for stat in self.session_request(league_settings())['fantasy_content']['league'][1]['settings'][0]['stat_modifiers']['stats']}
        for stat in self.session_request(league_settings())['fantasy_content']['league'][1]['settings'][0]['stat_categories']['stats']:
            stat = stat['stat']
            stat_id = stat['stat_id']
            stats[stat_id] = {'name': stat['name'], 'display_name': stat['display_name'], 'position_type': stat['position_type']}
            if stat_id in modifiers.keys():
                stats[stat_id]['value'] = modifiers[stat_id]['value']
            if 'is_only_display_stat' in list(stat.keys()):
                stats[stat_id]['display_only'] = 'Y'
            else:
                stats[stat_id]['display_only'] = 'F'
        return stats
    
    def get_team_positions(self, positions = {}):
        for position in self.session_request(league_settings())['fantasy_content']['league'][1]['settings'][0]['roster_positions']:
            position = position['roster_position']
            try:
                positions[position['position'].replace('W/R/T','FLEX')] = {'position_type':position['position_type'], 'count': position['count']}
            except:
                positions[position['position'].replace('W/R/T','FLEX')] = {'position_type': 'M', 'count': position['count'] }
        return positions

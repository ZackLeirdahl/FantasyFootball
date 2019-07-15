import json, os
from yahoo_oauth import OAuth2
from endpoints import *

class YahooFantasyAPI:
    def __init__(self):
        self.session = self.get_session()
        self.fmt = 'json'

    def get_session(self):
        oauth = OAuth2(None,None,from_file= r'fantasy_app\static\auth\oauth2.json')
        if not oauth.token_is_valid():
            oauth.refresh_access_token()
        return oauth.session

    def session_request(self, url):
        data = self.session.get(url, params={'format':self.fmt})
        return json.loads(data.text)
        
    def get_user_data(self):
        data = self.session_request(league_standings())['fantasy_content']['league'][1]['standings'][0]['teams']
        details = {}
        key_list = [0,1,2,5,18]
        for k in list(data.keys()):
            try:
                team_id = data[k]['team'][0][1]['team_id']
                details[team_id] = {}
                try:
                    t = data[k]['team'][0]
                    for li in key_list:
                        if li == 5:
                            details[team_id]['image'] = data[k]['team'][0][5]['team_logos'][0]['team_logo']['url']
                        elif li == 18:
                            manager = data[k]['team'][0][-1]['managers'][0]['manager']
                            details[team_id]['manager_id'] = manager['manager_id']
                            details[team_id]['nickname'] = manager['nickname']
                            details[team_id]['email'] = manager['email']
                        else:
                            if li == 0:
                                details[team_id]['team_key'] = t[li]['team_key']
                            elif li == 1:
                                details[team_id]['team_id'] = t[li]['team_id']
                            else:
                                details[team_id]['name'] = t[li]['name']
                except:
                    continue
            except:
                continue
        return details
    
    def get_matchup_data(self, team_id, week):
        data = self.session_request(team_matchups(team_id, week))['fantasy_content']['team'][1]['matchups']['0']['matchup']
        details = {}
        mathup_details = ['week', 'week_start', 'week_end', 'status', 'is_playoffs', 'is_consolation', 'is_matchup_recap_available']
        for k, v in data.items():
            if k in mathup_details:
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

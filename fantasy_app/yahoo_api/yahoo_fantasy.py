import json
from yahoo_oauth import OAuth2
from fantasy_app.yahoo_api.const import oauth_file
from fantasy_app.yahoo_api.endpoints import *

class YahooFantasyAPI:
    def __init__(self):
        self.session = self.get_session()
        self.fmt = 'json'

    def get_session(self):
        oauth = OAuth2(None,None,from_file=oauth_file)
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
            details[k] = {}
            try:
                t = data[k]['team'][0]
                for li in key_list:
                    if li == 5:
                        details[k]['image'] = data[k]['team'][0][5]['team_logos'][0]['team_logo']['url']
                    elif li == 18:
                        manager = data[k]['team'][0][-1]['managers'][0]['manager']
                        details[k]['manager_id'] = manager['manager_id']
                        details[k]['nickname'] = manager['nickname']
                        details[k]['email'] = manager['email']
                    else:
                        if li == 0:
                            details[k]['team_key'] = t[li]['team_key']
                        elif li == 1:
                            details[k]['team_id'] = t[li]['team_id']
                        else:
                            details[k]['name'] = t[li]['name']
            except:
                continue
        return details
    

       



#api.get_user_data()
#print(api.get_user_img('zackleirdahl@gmail.com'))
#api.session_request(league_standings())
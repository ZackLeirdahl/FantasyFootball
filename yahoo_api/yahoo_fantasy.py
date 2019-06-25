from yahoo_oauth import OAuth2
from const import oauth_file
from endpoints import *
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
        print(data.text)

api = YahooFantasyAPI()
api.session_request(league_players())
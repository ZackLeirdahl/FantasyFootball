from fantasy_app.yahoo_api.yahoo_fantasy import YahooFantasyAPI
from fantasy_app.yahoo_api.firebase import Firebase

class YAccess:
    def __init__(self):
        self.fb = Firebase()
        self.api = None
    
    def api_session(self):
        if self.api == None:
            self.api == YahooFantasyAPI()
    
    def get_user_data(self, username=None):
        data = self.fb.get_documents('team')
        for k in list(data.keys()):
            try:
                if data[k]['email'] == username:
                    return data[k]
            except:
                continue
        return None

import firebase_admin, os, pandas
from firebase_admin import credentials, firestore
from api import YahooFantasyAPI

class Firebridge(YahooFantasyAPI):
    def __init__(self, connect = True):
        firebase_admin.initialize_app(credentials.Certificate('fantasy_app//static//auth//firebase_auth.json'))
        self.fb = firestore.client()
        if connect:
            YahooFantasyAPI.__init__(self)

    def add_document(self, collection, key, data):
        self.fb.collection(collection).document(key).set(data)

    def remove_document(self, collection, key):
        for doc in self.fb.collection(collection).get():
            if doc.id == key: doc.reference.delete()

    def update_document(self, collection, key, data):
        self.fb.collection(collection).document(key).update(data)

    def get_documents(self, collection):
        return {doc.id: doc.to_dict() for doc in self.fb.collection(collection).get()}

    def get_document_ids(self, collection):
        return [doc.id for doc in self.fb.collection(collection).get()]

    def get_document(self, collection, key):
        return self.fb.collection(collection).document(key).get().to_dict() 

    def update_teams(self):
        for k, v in self.get_user_data().items():
            self.update_document('team', k, v)

    def get_user_likes(self, userid='1'):
        postids = []
        for k in list(self.get_documents('likes').keys()):
            k = k.split('-')
            if k[0] == str(userid):
                postids.append(k[1])
        return postids

    def add_season_matchups(self, keys = []):
        for team_id in self.get_document_ids('team'):
            for i in range(13):
                flag = True
                data = self.get_matchup_data(team_id, str(i+1))
                key = set(data[0].split('-'))
                for k in keys:
                    if k == key:
                        flag = False
                if flag:
                    keys.append(key)
                    self.add_document('matchups', data[0], data[1])
                    
    def update_season_matchups(self, keys = []):
        for team_id in self.get_document_ids('team'):
            for i in range(13):
                flag = True
                data = self.get_matchup_data(team_id, str(i+1))
                key = set(data[0].split('-'))
                for k in keys:
                    if k == key:
                        flag = False
                if flag:
                    keys.append(key)
                    self.update_document('matchups', data[0], data[1])

    def add_standings(self):
        for k, v in self.get_standings().items():
            self.add_document('standings',k,v)

    def update_standings(self):
        for k, v in self.get_standings().items():
            self.update_document('standings',k,v)

    def add_players(self):
        for k, v in self.get_player_ids().items():
            for kk, vv in self.get_player_description(v).items():
                self.add_document('players',kk,vv)
    
    def add_stat_categories(self):
        for k, v in get_stat_categories().items():
            self.add_document('stat_categories', str(k), v)
    
    def update_stat_categories(self):
        for k, v in self.get_stat_categories().items():
            self.update_document('stat_categories', str(k), v)
    
    def add_roster_positions(self):
        for k, v in self.get_team_positions().items():
            self.add_document('roster_positions', k, v)

    def update_roster_positions(self):
        for k, v in self.get_team_positions().items():
            self.update_document('roster_positions', k, v)
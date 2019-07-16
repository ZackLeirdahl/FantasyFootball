import firebase_admin, os
from firebase_admin import credentials, firestore
from api import YahooFantasyAPI

class Firebridge(YahooFantasyAPI):
    def __init__(self, connect = True):
        firebase_admin.initialize_app(credentials.Certificate(r'fantasy_app/static/auth/firebase_auth.json'))
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

    def update_teams(self):
        for k, v in self.get_user_data().items():
            self.fb.update_document('team', k, v)

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
        standings = self.get_standings()
        for k, v in standings.items():
            self.add_document('standings',k,v)

    def update_standings(self):
        standings = self.get_standings()
        for k, v in standings.items():
            self.update_document('standings',k,v)

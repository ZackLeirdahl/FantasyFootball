import datetime, time, math, firebase_admin, os, pandas
from flask import g, current_app
from firebase_admin import credentials, firestore
from firebase_admin import db as fb

def get_fdb():
    if (not len(firebase_admin._apps)):
        firebase_admin.initialize_app(credentials.Certificate(os.path.dirname(__file__) + r'\static\auth\firebase_auth.json'), options= {'databaseURL': 'https://fantasyfootball-ee95c.firebaseio.com'})
    if 'fb' not in g:
        g.fb = firestore.client()
    return g.fb

def get_posttime_data(td):
    if td < 60:
        return 'just now'
    elif td < 3600:
        return str(math.trunc(td / 60)) + 'm'
    elif td < 86400:
        return str(math.trunc(td / 3600)) + 'h'
    else:
        return str(math.trunc(td / 86400)) + 'd'

def match_name(name, last_name, first_name):
    names = name.split(' ')
    if len(names) == 1:
        if first_name[:len(name)] == name:
            return True
        elif last_name[:len(name)] == name:
            return True
    else:
        if first_name == names[0] and last_name[:len(names[1])] == names[1]:
            return True
    return False
    
class Firedata:
    def __init__(self, client = None):
        self.fb = get_fdb()

    def add_document_auto_key(self, collection, data):
        self.fb.collection(collection).add(data)
        
    def add_document(self, collection, key, data):
        self.fb.collection(collection).document(key).set(data)

    def remove_document(self, collection, key):
        for doc in self.fb.collection(collection).get():
            if doc.id == key: doc.reference.delete()

    def update_document(self, collection, key, data):
        self.fb.collection(collection).document(key).update(data)

    def get_documents(self, collection):
        return {doc.id: doc.to_dict() for doc in self.fb.collection(collection).get()}

    def get_document(self, collection, key):
        return self.fb.collection(collection).document(key).get().to_dict() 

    def generate_key(self, collection):
        if len(list(self.get_documents(collection).keys())) != 0:
            return str(int(max(list(self.get_documents(collection).keys()))) + 1)
        else:
            return '1'
    
    def like_post(self, id, userid):
        self.add_document('likes', str(userid) + '-' + str(id),{'liked': 1})
        post = self.get_document('posts',str(id))
        post['likes'] += 1
        self.update_document('posts', str(id), post)

    def unlike_post(self, id, userid):
        self.remove_document('likes', str(userid) + '-' + str(id))
        post = self.get_document('posts',str(id))
        post['likes'] -= 1
        self.update_document('posts', str(id), post)

    def add_post(self, data):
        self.add_document('posts', self.generate_key('posts'), data)

    def add_comment(self, data):
        self.add_document('comments', self.generate_key('comments'), data)
        post = self.get_document('posts',str(data['postid']))
        post['comments'] += 1
        self.update_document('posts', str(data['postid']), post)

    def delete_post(self, id):
        self.remove_document('posts', str(id))
        for k, v in self.get_documents('comments').items():
            if v['postid'] == str(id):
                self.remove_document('comments', k)
        for k in list(self.get_documents('likes').keys()):
            if k.split('-')[1] == str(id):
                self.remove_document('likes', k)

    def get_user_likes(self, userid):
        postids = []
        for k in list(self.get_documents('likes').keys()):
            k = k.split('-')
            if k[0] == str(userid):
                postids.append(k[1])
        return postids

    def get_post(self, key):
        document = self.get_document('posts',str(key))
        document['created'] = get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) - document['time'])
        document['id'] = key
        return document

    def get_posts(self):
        posts = []
        data = self.get_documents('posts')
        for k, v in data.items():
            v['created'] = get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) - v['time'])
            v.update({'id': k})
            posts.append(v)
        return sorted(posts,key=lambda k: k['time'], reverse=True)
    
    def get_comments(self):
        comments = []
        data = self.get_documents('comments')
        for k, v in data.items():
            v['created'] = get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) - v['time'])
            v.update({'id': k})
            comments.append(v)
        return sorted(comments,key=lambda k: k['time'], reverse=True)
        
    def get_yahoo_user(self, username):
        data = self.get_documents('team')
        for k in list(data.keys()):
            if data[k]['email'] == username:
                return data[k]
        return None

    def update_yahoo_user(self, username, password):
        data = self.get_documents('team')
        for k in list(data.keys()):
            if data[k]['email'] == username:
                self.update_document('teams',str(k), {'username': username, 'password': password})

    def check_yahoo_user(self, username):
        data = self.get_documents('team')
        for k in list(data.keys()):
            if data[k]['username'] == username:
                return True
        return False

    def get_matchups(self, week=None):
        team_stats = []
        matchups = []
        if week == None:
            week = self.get_week()
        teams = self.get_documents('team')
        for k, v in self.get_documents('matchups').items():
            if k.split('-')[0] == week:
                team_ids = k.split('-')[1:3]
                matchups.append(team_ids)
                temp_matchup = []
                for team_id in team_ids:
                    temp = v[team_id]
                    temp.update(teams[team_id])
                    temp_matchup.append(temp)
                team_stats.append(temp_matchup)
        for ts in team_stats:
            ts[0]['percent_chance'] = str(ts[0]['win_probability'] * 100) +'%'
            ts[1]['percent_chance'] = str(ts[1]['win_probability'] * 100) +'%'
            if ts[1]['win_probability'] <= 0.5:
                ts[1].update({'opacity': 0.5, 'class': 'bg-danger'})
                ts[0].update({'opacity': ts[0]['win_probability'], 'class': 'bg-success'})
            else:
                ts[0].update({'opacity': 0.5, 'class': 'bg-danger'})
                ts[1].update({'opacity': ts[1]['win_probability'], 'class': 'bg-success'})
        return team_stats

    def get_standings(self):
        standings = []
        teams = self.get_documents('team')
        for k,v in self.get_documents('standings').items():
            temp = v
            temp.update(teams[k])
            standings.append(temp)
        return sorted(standings,key=lambda k: int(k['rank']))
    
    def get_week(self):
        today = datetime.date.today().toordinal()
        week_one_end = datetime.date(2019,9,9).toordinal()
        if today <= week_one_end:
            return '1'
        else:
            return str(math.ceil((today - week_one_end)/7))

    def get_roster_positions(self):
        data = ['QB','WR','WR','RB','RB','TE','FLEX','K','DEF','BN','BN','BN','BN','BN','BN']
        return data
    
    def get_players(self):
        if not os.path.isfile(os.path.dirname(__file__) + r'\static\temp\players.csv'):
            players = self.get_documents('players')
            df = pandas.DataFrame(players)
            df.to_csv(os.path.dirname(__file__) + r'\static\temp\players.csv')
            return players
        else:
            return pandas.read_csv(os.path.dirname(__file__) + r'\static\temp\players.csv', header = None, index_col=0).to_dict()
    
    def get_players_filter_data(self):
        teams = []
        for k, v in self.get_players().items():
            if v['editorial_team_abbr'].upper() not in teams:
                teams.append(v['editorial_team_abbr'].upper())
        teams.sort()
        return {'teams': teams, 'positions':['QB','RB','WR','TE','FLEX','DEF','K']}

    def get_players_filter(self, pos=None, team=None, player=None):
        players = {}
        if pos + team + player == '':
            return self.get_players()
        for k, v in self.get_players().items():
            if pos != '':
                if v['display_position'] == pos:
                    if team != '':
                        if v['editorial_team_abbr'].upper() == team:
                            if player != '':
                                if match_name(player.lower(), v['last_name'].lower(), v['first_name'].lower()):
                                    players[k] = v
                            else:
                                players[k] = v
                    elif player != '':
                        if match_name(player.lower(), v['last_name'].lower(), v['first_name'].lower()):
                            players[k] = v
                    else:
                        players[k] = v
            elif team != '':
                if v['editorial_team_abbr'].upper() == team:
                    if player != '':
                        if match_name(player.lower(), v['last_name'].lower(), v['first_name'].lower()):
                            players[k] = v
                    else:
                        players[k] = v
            else:
                if match_name(player.lower(), v['last_name'].lower(), v['first_name'].lower()):
                    players[k] = v
        if len(players) == 0:
            return self.get_players()
        return players
    
    def get_teams_temp(self):
        if not os.path.isfile(os.path.dirname(__file__) + r'\static\temp\teams.csv'):
            data = self.get_documents('team')
            df = pandas.DataFrame(data)
            df.to_csv(os.path.dirname(__file__) + r'\static\temp\teams.csv')
            return data
        else:
            return pandas.read_csv(os.path.dirname(__file__) + r'\static\temp\teams.csv', index_col=0).to_dict()
        
    def get_team_data(self, team_id):
        data = self.get_document('team', str(team_id))
        data.update(self.get_document('standings', str(team_id)))
        data['points_week'] = int(data['points_for']) / int(self.get_week())
        return data







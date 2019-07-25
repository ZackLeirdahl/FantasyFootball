from .db import get_fdb
import datetime, time, math

def get_posttime_data(td):
    if td < 60:
        return 'just now'
    elif td < 3600:
        return str(math.trunc(td / 60)) + 'm'
    elif td < 86400:
        return str(math.trunc(td / 3600)) + 'h'
    else:
        return str(math.trunc(td / 86400)) + 'd'


class Firedata:
    def __init__(self):
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
        for doc in self.fb.collection(collection).get():
            if doc.id == key:
                return doc.to_dict()
        return None

class Firefeed(Firedata):
    def __init__(self):
        Firedata.__init__(self)
    
    def generate_key(self, collection):
        return str(len(self.get_documents(collection).keys()) + 1)
    
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
        print(sorted(comments,key=lambda k: k['time'], reverse=True))
        return sorted(comments,key=lambda k: k['time'], reverse=True)

class Fireleague(Firedata):
    def __init__(self):
        Firedata.__init__(self)
    
    def get_teams(self):
        return [v for k, v in self.get_documents('team').items()]
    
    def get_yahoo_user(self, username):
        data = self.get_documents('team')
        for k in list(data.keys()):
            if data[k]['email'] == username:
                return data[k]
        return None

    def get_matchups(self):
        team_stats = []
        matchups = []
        week = self.get_week()
        teams = self.get_documents('team')
        for k, v in self.get_documents('matchups').items():
            if k[len(week)] == week:
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
        return '1'

    def get_roster_positions(self):
        data = self.get_documents('roster_positions')
        print(data)
        return data


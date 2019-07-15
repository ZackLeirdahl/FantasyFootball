import math
import pandas as pd
from .db import get_fdb

def get_posttime_data(td):
    if td < 60:
        return 'just now'
    elif td < 3600:
        return str(math.trunc(td / 60)) + 'm'
    elif td < 86400:
        return str(math.trunc(td / 3600)) + 'h'
    else:
        return str(math.trunc(td / 86400)) + 'd'

def add_document(collection, key, data):
    get_fdb().collection(collection).document(key).set(data)

def remove_document(collection, key):
    for doc in get_fdb().collection(collection).get():
        if doc.id == key: doc.reference.delete()

def update_document(collection, key, data):
    get_fdb().collection(collection).document(key).update(data)

def get_documents(collection):
    return {doc.id: doc.to_dict() for doc in get_fdb().collection(collection).get()}

def get_document(collection, key):
    for doc in get_fdb().collection(collection).get():
        if doc.id == key:
            return doc.to_dict()
    return None

def get_yahoo_user(username):
    data = get_documents('team')
    for k in list(data.keys()):
        if data[k]['email'] == username:
            return data[k]
    return None

def get_matchups():
    team_stats = {}
    matchups = []
    week = get_week()
    teams = get_documents('team')
    data = get_documents('matchups')
    for k, v in data.items():
        if k[len(week)] == week:
            team_ids = k.split('-')[1:3]
            matchups.append(team_ids)
            for team_id in team_ids:
                team_stats[team_id] = v[team_id]
                team_stats[team_id].update(teams[team_id])
    return pd.DataFrame(team_stats)


def get_week():
    return '1'
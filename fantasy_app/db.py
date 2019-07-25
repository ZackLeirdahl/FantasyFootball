import sqlite3, click, firebase_admin, os
from flask import current_app, g
from flask.cli import with_appcontext
from firebase_admin import credentials, firestore
from firebase_admin import db as fb
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_fdb():
    if (not len(firebase_admin._apps)):
        firebase_admin.initialize_app(credentials.Certificate(os.path.dirname(__file__) + r'\static\auth\firebase_auth.json'),
                options= {'databaseURL': 'https://fantasyfootball-ee95c.firebaseio.com'})
    if 'fb' not in g:
        g.fb = firestore.client()
    return g.fb
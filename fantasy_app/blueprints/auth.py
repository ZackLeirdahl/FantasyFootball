import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from ..db import get_db
from ..firedata import Fireleague, Firefeed

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.fl = Fireleague()
    g.ff = Firefeed()
    if user_id is None:
        g.user = None
        g.teams = None
        g.upload_folder = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        g.teams = g.fl.get_teams()
        g.upload_folder = r'C:\Users\zleirdahl\Documents\GitHub\FantasyFootball\fantasy_app\static\upload'
        
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        if error is None:
            fl = Fireleague()
            user = fl.get_yahoo_user(username)
            db.execute('INSERT INTO user (username, password, image, name, nickname, teamid) VALUES (?, ?, ?, ?, ?, ?)',(username, generate_password_hash(password),user['image'],user['name'], user['nickname'], user['team_id']))
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login(error = None):
    if request.method == 'POST':
        user = get_db().execute('SELECT * FROM user WHERE username = ?', (request.form['username'],)).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], request.form['password']):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

import functools, firebase_admin, os
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from ..firedata import Firedata, get_fdb
from firebase_admin import credentials, firestore
from firebase_admin import db as fb
bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.before_app_request
def load_logged_in_user():
    g.fd = Firedata()
    if session.get('username') is None:
        g.user = None
        g.teams = None
        g.upload_folder = None
    else:
        g.user = g.fd.get_yahoo_user(session.get('username'))
        g.teams = g.fd.get_teams_temp()
        g.upload_folder = 'C:\\Users\\zleirdahl\\Documents\\GitHub\\FantasyFootball\\fantasy_app\\static\\upload'


@bp.route('/register', methods=('GET', 'POST'))
def register(error = None):
    if request.method == 'POST':
        if g.fd.check_yahoo_user(request.form['username']):
            error = 'User {} is already registered.'.format(request.form['username'])
        if error is None:
            g.fd.update_yahoo_user(request.form['username'],request.form['password'])
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('POST', ))
def login():
    user = g.fd.get_yahoo_user(request.form['username'])
    if user is None:
        flash('Incorrect username.')
    elif user['password'] != request.form['password']:
        flash('Incorrect password.')
    else:
        session.clear()
        session['username'] = user['username']
        return redirect(url_for('league.standings'))
    return redirect(url_for('blog.index'))
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

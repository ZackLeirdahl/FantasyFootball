import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from .auth import login_required
bp = Blueprint('league', __name__, url_prefix='/league')

@bp.route('/matchups', methods=('GET', 'POST'))
@login_required
def matchups():
    week = None
    weeks = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
    if request.method == 'POST':
        week = request.form['week']
        weeks.remove(week)
        matchups = g.fd.get_matchups(week)
    else:
        matchups=g.fd.get_matchups()
    return render_template('league/matchups.html', matchups=matchups, week=week, current_week=g.fd.get_week(), weeks=weeks)

@bp.route('/standings', methods=('GET', 'POST'))
@login_required
def standings():
    g.fd.get_teams_temp()
    return render_template('league/standings.html', standings=g.fd.get_standings())

@bp.route('/<int:id>/teams', methods=('GET', 'POST'))
@login_required
def teams(id):
    return render_template('league/teams.html', roster_positions = g.fd.get_roster_positions(), team=g.fd.get_team_data(str(id)))

@bp.route('/players', methods=('GET', 'POST'))
@login_required
def players():
    filters = {'position': None, 'team': None, 'player': None}
    if request.method == "POST":
        if request.form['position'] != '':
            filters['position'] = request.form['position']
        if request.form['team'] != '':
            filters['team'] = request.form['team']
        if request.form['player'] != '':
            filters['player'] = request.form['player']
        players = g.fd.get_players_filter(request.form['position'], request.form['team'], request.form['player'])
    else:
        players=g.fd.get_players()
    return render_template('league/players.html', players=players, filter_data=g.fd.get_players_filter_data(), filters=filters)

@bp.route('/home', methods=('GET', 'POST'))
@login_required
def home():
    return render_template('league/home.html')
    
@bp.route('/weekly_awards', methods=('GET', 'POST'))
@login_required
def weekly_awards():
    return render_template('league/weekly_awards.html')

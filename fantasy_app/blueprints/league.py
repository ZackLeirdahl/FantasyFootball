import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from .auth import login_required

bp = Blueprint('league', __name__, url_prefix='/league')

@bp.route('/matchups', methods=('GET', 'POST'))
@login_required
def matchups():
    return render_template('league/matchups.html', matchups=g.fl.get_matchups())

@bp.route('/standings', methods=('GET', 'POST'))
@login_required
def standings():
    return render_template('league/standings.html', standings=g.fl.get_standings())

@bp.route('/<int:id>/teams', methods=('GET', 'POST'))
@login_required
def teams(id):
    return render_template('league/teams.html', roster_positions = g.fl.get_roster_positions(), team=g.fl.get_document('team', str(id)))

@bp.route('/players', methods=('GET', 'POST'))
@login_required
def free_agents():
    return render_template('league/players.html')

@bp.route('/weekly_awards', methods=('GET', 'POST'))
@login_required
def weekly_awards():
    return render_template('league/weekly_awards.html')
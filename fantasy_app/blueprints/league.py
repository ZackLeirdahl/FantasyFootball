import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .auth import login_required
from ..db import get_db, get_fdb
from ..util import get_matchups, get_standings
bp = Blueprint('league', __name__, url_prefix='/league')


@bp.route('/matchups', methods=('GET', 'POST'))
@login_required
def matchups():
    matchups = get_matchups()
    return render_template('league/matchups.html', matchups=matchups)

@bp.route('/standings', methods=('GET', 'POST'))
@login_required
def standings():
    standings = get_standings()
    return render_template('league/standings.html', standings=standings)

@bp.route('/teams', methods=('GET', 'POST'))
@login_required
def teams():
    return render_template('league/standings.html')

@bp.route('/free_agents', methods=('GET', 'POST'))
@login_required
def free_agents():
    return render_template('league/free_agents.html')

@bp.route('/weekly_awards', methods=('GET', 'POST'))
@login_required
def weekly_awards():
    return render_template('league/weekly_awards.html')
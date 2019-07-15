import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .auth import login_required
from ..db import get_db, get_fdb
from ..util import get_matchups, get_week, get_documents
bp = Blueprint('matchups', __name__, url_prefix='/matchups')


@bp.route('/view', methods=('GET', 'POST'))
@login_required
def view():
    matchups = get_matchups()

    return render_template('matchups/view.html')

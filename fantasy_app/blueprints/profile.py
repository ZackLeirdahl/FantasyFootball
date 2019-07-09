import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from fantasy_app.blueprints.auth import login_required
from fantasy_app.db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/viewprofile', methods=('GET', 'POST'))
@login_required
def view_profile():
    return render_template('profile/viewprofile.html')
import functools
import random, json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)
from .auth import login_required
from ..db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/viewprofile', methods=('GET', 'POST'))
@login_required
def view_profile():
    return render_template('profile/viewprofile.html')


@bp.route('/receiver', methods = ('POST',))
def worker():
    data = request.form['mydata']
    print(data)
    return data
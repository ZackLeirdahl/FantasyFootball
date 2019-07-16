import datetime, time, uuid
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, current_app)
from werkzeug.exceptions import abort
from .auth import login_required
from ..db import get_db, get_fdb
from ..const import *
from ..util import *
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts=db.execute(get_posts).fetchall()
    posttimes = [{'id': posts[i][0], 'time': get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) + 18000 - time.mktime(posts[i][3].timetuple()))} for i in range(len(posts))]
    comments = db.execute(get_comments).fetchall()
    commenttimes = [{'id': comments[i][0], 'time': get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) + 18000 - time.mktime(comments[i][5].timetuple()))} for i in range(len(comments))]
    return render_template('blog/index.html', posts=posts, posttimes=posttimes, comments=comments, commenttimes=commenttimes)

@bp.route('/feed', methods=('GET', 'POST'))
def feed():
    if request.method == "POST":
        db = get_db()
        comment = request.form['comment']
        id = request.form['id']
        error = None
        if not comment:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db.execute(insert_post_comment,(id, g.user['id'],g.user['name'], comment))
            db.commit()
            db.execute(update_post_comments,(id,))
            db.commit()
        return redirect(url_for('blog.feed'))
    db = get_db()
    posts=db.execute(get_posts).fetchall()
    posttimes = [{'id': posts[i][0], 'time': get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) + 18000 - time.mktime(posts[i][3].timetuple()))} for i in range(len(posts))]
    comments = db.execute(get_comments).fetchall()
    commenttimes = [{'id': comments[i][0], 'time': get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) + 18000 - time.mktime(comments[i][5].timetuple()))} for i in range(len(comments))]
    return render_template('blog/feed.html', posts=posts, posttimes=posttimes, comments=comments, commenttimes=commenttimes)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create(error = None):
    if request.method == 'POST':
        if not request.form['title']:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(insert_post,(request.form['title'],request.form['body'],g.user['id'], 0, 0, 0))
            db.commit()
            return redirect(url_for('blog.feed'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute('SELECT p.id, title, body, created, author_id, name, likes, dislikes, comments FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?',(id,)).fetchone()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required.')
        else:
            db = get_db()
            db.execute(update_post,(request.form['title'], request.form['body'], id))
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=get_post(id))

@bp.route('/<int:id>/delete', methods=('POST','GET'))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(delete_post, (id,))
    db.commit()
    return redirect(url_for('blog.feed'))


def set_likes_data(id):
    db = get_db()
    likes = int(db.execute(get_likes_count,(id,)).fetchone()[0])
    dislikes = int(db.execute(get_dislikes_count,(id,)).fetchone()[0])
    comments = int(db.execute(get_comments_count,(id,)).fetchone()[0])
    db.execute(update_post_counts, (likes,dislikes,comments,id,))
    db.commit()

@bp.route('/<int:id>/<int:action>/like', methods=('GET','POST'))
@login_required
def like(id, action):
    db = get_db()
    users = [p[0] for p in db.execute(get_post_likes, (id,)).fetchall()]
    if g.user['id'] not in users:
        db.execute(insert_user_like,(g.user['id'], id, action, 0))
        db.commit()
    else:
        if action == 1:
            db.execute(update_user_likes_like,(g.user['id'], id,))
            db.commit()
        else:
            db.execute(update_user_likes_unlike,(g.user['id'], id,))
            db.commit()
    set_likes_data(id)
    return redirect(url_for('blog.feed'))

@bp.route('/<int:id>/<int:action>/dislike', methods=('GET','POST'))
@login_required
def dislike(id, action):
    db = get_db()
    users = [p[0] for p in db.execute(get_post_likes, (id,)).fetchall()]
    if g.user['id'] not in users:
        db.execute(insert_user_like,(g.user['id'], id, 0, action))
        db.commit()
    else:
        if action == 1:
            db.execute(update_user_likes_dislike,(g.user['id'], id,))
            db.commit()
        else:
            db.execute(update_user_likes_unlike,(g.user['id'], id,))
            db.commit()
    set_likes_data(id)
    return redirect(url_for('blog.feed'))

@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == "POST":
        description = request.form['description']
        file = request.form['file']
        if not file:
            flash('Image is required.')
        else:
            add_document('post_image', str(g.user['id']) + '_' + str(uuid.uuid1())[:8], {'file': file , 'description': description })
            return redirect(url_for('blog.feed'))
    return render_template('blog/upload.html')
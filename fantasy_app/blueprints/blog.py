import datetime, time
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, current_app)
from werkzeug.exceptions import abort
from fantasy_app.blueprints.auth import login_required
from fantasy_app.db import get_db
from fantasy_app.forms import CreatePostForm, PostCommentForm, UpdatePostForm, ViewPostForm
from fantasy_app.const import *
from fantasy_app.util import *
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts=db.execute(get_posts).fetchall()
    posttimes = [{'id': posts[i][0], 'time': get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) + 18000 - time.mktime(posts[i][3].timetuple()))} for i in range(len(posts))]
    comments = db.execute(get_comments).fetchall()
    commenttimes = [{'id': comments[i][0], 'time': get_posttime_data(time.mktime(datetime.datetime.today().timetuple()) + 18000 - time.mktime(comments[i][5].timetuple()))} for i in range(len(comments))]
    return render_template('blog/index.html', posts=posts, posttimes=posttimes, comments=comments, commenttimes=commenttimes)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CreatePostForm()
    if request.method == 'POST':
        title = form.title.data
        body = form.body.data
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(insert_post,(title, body, g.user['id'], 0, 0, 0))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html', title='New Post', form=form)

def get_post(id, check_author=True):
    post = get_db().execute('SELECT p.id, title, body, created, author_id, name, likes, dislikes, comments FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?',(id,)).fetchone()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    try:
        if check_author and post['author_id'] != g.user['id']:
            abort(403)
    except:
        return post
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    form = UpdatePostForm()
    if request.method == 'POST':
        title = form.title.data
        body = form.body.data
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(update_post,(title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))
    form.body.data = post['body']
    form.title.data = post['title']
    return render_template('blog/update.html', post=post, form=form)

@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    post = get_post(id)
    form = ViewPostForm()
    if request.method == 'POST':
        return redirect(url_for('blog.index'))
    form.body.data = post['body']
    form.title.data = post['title']
    return render_template('blog/view.html', post=post, form=form)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(delete_post, (id,))
    db.commit()
    return redirect(url_for('blog.index'))

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
    return redirect(url_for('blog.index'))

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
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/comment', methods=('GET','POST'))
@login_required
def comment(id):
    form = PostCommentForm()
    if request.method == "POST":
        db = get_db()
        comment = form.comment.data
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
        return redirect(url_for('blog.index'))
    return render_template('blog/comment.html', form=form)
import datetime, time, json, random, string, os
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, current_app)
from werkzeug.exceptions import abort
from werkzeug import secure_filename
from .auth import login_required
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    return render_template('blog/index.html')

@bp.route('/feed', methods=('GET', 'POST'))
def feed():
    posts=g.ff.get_posts()
    return render_template('blog/feed.html', posts=posts,comments=g.ff.get_comments(), user_likes=g.ff.get_user_likes(g.user['id']))

@bp.route('/<int:id>/comment', methods=('POST',))
def comment(id):
    if not request.form['commentText']:
        flash('Comment text is required.')
    else:
        print(request.form['commentText'])
        g.ff.add_comment({'postid': str(id), 'userid': g.user['id'], 'name': g.user['name'], 'comment': request.form['commentText'], 'time': time.mktime(datetime.datetime.today().timetuple())})
    return redirect(url_for('blog.feed'))

@bp.route('/create', methods=('POST',))
@login_required
def create():
    if not request.form['title']:
        flash('Title is required.')
    else:
        uid = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        g.ff.add_post(data = {'author_id':g.user['id'],'uid': uid, 'name': g.user['name'], 'type':'text', 'time': time.mktime(datetime.datetime.today().timetuple()), 'title': request.form['title'], 'body': request.form['body'], 'likes': 0, 'comments': 0})
    return redirect(url_for('blog.feed'))

@bp.route('/<int:id>/update', methods=('POST',))
@login_required
def update(id):
    if not request.form['title']:
        flash('Title is required.')
    else:
        g.ff.update_document('posts', str(id), {'title':request.form['title'], 'body': request.form['body']})
    return redirect(url_for('blog.feed'))


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    g.ff.delete_post(id)
    try:
        os.remove(os.path.join(g.upload_folder,request.form['filename']))
    except:
        pass
    return redirect(url_for('blog.feed'))


@bp.route('/like', methods=('POST',))
@login_required
def like():
    if int(request.form['action']) == 1:
        g.ff.like_post(request.form['id'], g.user['id'])
    else:
        g.ff.unlike_post(request.form['id'], g.user['id'])
    return 'Success'

@bp.route('/uploadUpdate', methods=('POST',))
@login_required
def uploadUpdate(id):
    file = request.files['file']
    filename = secure_filename(file.filename)
    if check_extension(filename):
        file.save(os.path.join(g.upload_folder, filename))
        g.ff.update_document('posts',str(id), {'filename': filename, 'description': request.form['description']})
    return redirect(url_for('blog.feed'))

@bp.route('/upload', methods=('POST',))
@login_required
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    if check_extension(filename):
        file.save(os.path.join(g.upload_folder, filename))
        uid = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        g.ff.add_post(data = {'author_id':g.user['id'],'uid': uid, 'name': g.user['name'], 'type':'image', 'time': time.mktime(datetime.datetime.today().timetuple()), 'description': request.form['description'], 'filename': filename, 'likes': 0, 'comments': 0})
    return redirect(url_for('blog.feed'))

def check_extension(filename):
    if filename.split('.')[-1] in ['jpg','png','svg','gif','jpeg','pdf']:
        return True
    flash('The file extension needs to be jpg, jpeg, svg, png, gif or pdf.')
    return False
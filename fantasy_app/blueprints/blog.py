import datetime, time, random, string, os
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, current_app)
from werkzeug import secure_filename
from .auth import login_required
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    return render_template('blog/index.html')

@bp.route('/feed', methods=('GET', 'POST'))
def feed():
    posts=g.fd.get_posts()
    return render_template('blog/feed.html', posts=posts,comments=g.fd.get_comments(), user_likes=g.fd.get_user_likes(g.user['team_id']), amounts=['5','10','15','20','25'])

@bp.route('/<int:id>/comment', methods=('POST',))
def comment(id):
    if not request.form['commentText']:
        flash('Comment text is required.')
    else:
        g.fd.add_comment({'postid': str(id), 'userid': str(g.user['team_id']), 'name': g.user['name'], 'comment': request.form['commentText'], 'time': time.mktime(datetime.datetime.today().timetuple())})
    return redirect(url_for('blog.feed'))

@bp.route('/create', methods=('POST',))
@login_required
def create():
    if not request.form['title']:
        flash('Title is required.')
    else:
        uid = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        g.fd.add_post(data = {'author_id': str(g.user['team_id']),'uid': uid, 'name': g.user['name'], 'type':'text', 'time': time.mktime(datetime.datetime.today().timetuple()), 'title': request.form['title'], 'body': request.form['body'], 'likes': 0, 'comments': 0})
    return redirect(url_for('blog.feed'))

@bp.route('/update', methods=('POST',))
@login_required
def update():
    if not request.form['title']:
        flash('Title is required.')
    else:
        g.fd.update_document('posts', str(request.form['id']), {'title':request.form['title'], 'body': request.form['body']})
    return redirect(url_for('blog.feed'))

@bp.route('/delete', methods=('POST',))
@login_required
def delete():
    g.fd.delete_post(str(request.form['id']))
    try:
        os.remove(os.path.join(g.upload_folder,request.form['filename']))
    except:
        pass
    return redirect(url_for('blog.feed'))

@bp.route('/like', methods=('POST',))
@login_required
def like():
    if int(request.form['action']) == 1:
        g.fd.like_post(request.form['id'], g.user['team_id'])
    else:
        g.fd.unlike_post(request.form['id'], g.user['team_id'])
    return 'Success'

@bp.route('/uploadUpdate', methods=('POST',))
@login_required
def uploadUpdate():
    file = request.files['file']
    if check_extension(secure_filename(file.filename)):
        file.save(os.path.join('C:\\Users\\zleirdahl\\Documents\\GitHub\\FantasyFootball\\fantasy_app\\static\\upload', secure_filename(file.filename)))
        g.fd.update_document('posts',str(request.form['id']), {'filename': filename, 'description': request.form['description']})
    return redirect(url_for('blog.feed'))

@bp.route('/upload', methods=('POST',))
@login_required
def upload():
    file = request.files['file']
    if check_extension(secure_filename(file.filename)):
        file.save(os.path.join('C:\\Users\\zleirdahl\\Documents\\GitHub\\FantasyFootball\\fantasy_app\\static\\upload', secure_filename(file.filename)))
        uid = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        g.fd.add_post(data = {'author_id': str(g.user['team_id']),'uid': uid, 'name': g.user['name'], 'type':'image', 'time': time.mktime(datetime.datetime.today().timetuple()), 'description': request.form['description'], 'filename': file.filename, 'likes': 0, 'comments': 0})
    return redirect(url_for('blog.feed'))

def check_extension(filename):
    if filename.split('.')[-1] in ['jpg','png','svg','gif','jpeg','pdf']:
        return True
    flash('The file extension needs to be jpg, jpeg, svg, png, gif or pdf.')
    return False

@bp.route('/bet', methods=('POST',))
@login_required
def bet():
    return redirect(url_for('blog.feed'))
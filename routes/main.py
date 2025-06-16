from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from datetime import datetime
from models import Post, Notification, User
from __init__ import db

main_bp = Blueprint('main', __name__)

def create_notification(user_id, content, link=None):
    notification = Notification(user_id=user_id, content=content, link=link)
    db.session.add(notification)
    db.session.commit()

@main_bp.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main_bp.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date_created.desc()).all()
    return render_template('notifications.html', notifications=notifications)

@main_bp.route('/notifications/mark-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        flash('Bạn không thể đánh dấu thông báo này là đã đọc!', 'danger')
        return redirect(url_for('main.notifications'))
    notification.is_read = True
    db.session.commit()
    return redirect(url_for('main.notifications'))

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route("/search")
def search():
    query = request.args.get('q')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).order_by(Post.date_posted.desc()).all()
    else:
        posts = []
    return render_template('search.html', posts=posts, query=query) 
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import Post, Notification, User
from __init__ import db
from sqlalchemy import or_, func

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

@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    sort = request.args.get('sort', 'newest')
    time_filter = request.args.get('time', 'all')
    type_filter = request.args.get('type', 'all')
    
    if not query:
        return redirect(url_for('main.home'))
    
    # Base query
    posts_query = Post.query.filter(
        Post.title.ilike(f'%{query}%')
    )
    
    # Apply time filter
    if time_filter != 'all':
        now = datetime.utcnow()
        if time_filter == 'day':
            posts_query = posts_query.filter(Post.date_posted >= now - timedelta(days=1))
        elif time_filter == 'week':
            posts_query = posts_query.filter(Post.date_posted >= now - timedelta(weeks=1))
        elif time_filter == 'month':
            posts_query = posts_query.filter(Post.date_posted >= now - timedelta(days=30))
    
    # Apply type filter
    if type_filter == 'image':
        posts_query = posts_query.filter(Post.image_path.isnot(None))
    elif type_filter == 'text':
        posts_query = posts_query.filter(Post.image_path.is_(None))
    
    # Apply sorting
    if sort == 'oldest':
        posts_query = posts_query.order_by(Post.date_posted.asc())
    elif sort == 'popular':
        # Order by the number of likes
        posts_query = posts_query.outerjoin(Post.likes).group_by(Post.id).order_by(func.count(Post.likes).desc())
    else:  # newest
        posts_query = posts_query.order_by(Post.date_posted.desc())
    
    posts = posts_query.all()
    return render_template('search.html', posts=posts) 
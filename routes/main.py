from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import Post, Notification, User, Category
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
    categories = Category.query.order_by(Category.name).all()
    total_posts = Post.query.count()
    total_users = User.query.count()
    return render_template('home.html', posts=posts, categories=categories, total_posts=total_posts, total_users=total_users)

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
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Bạn không thể đánh dấu thông báo này là đã đọc!'}), 403
        else:
            flash('Bạn không thể đánh dấu thông báo này là đã đọc!', 'danger')
            return redirect(url_for('main.notifications'))
    
    notification.is_read = True
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'notification_id': notification_id})
    else:
        flash('Thông báo đã được đánh dấu là đã đọc!', 'success')
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
    category_filter = request.args.get('category', 'all')
    
    if not query:
        return redirect(url_for('main.home'))
    
    posts_query = Post.query.filter(
        Post.title.ilike(f'%{query}%')
    )
    
    if category_filter != 'all':
        posts_query = posts_query.filter(Post.category_id == int(category_filter))
    
    # Apply time filter
    if time_filter != 'all':
        now = datetime.utcnow()
        if time_filter == 'day':
            start_of_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            posts_query = posts_query.filter(Post.date_posted >= start_of_day)
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
    categories = Category.query.order_by(Category.name).all()
    return render_template('search.html', posts=posts, categories=categories) 
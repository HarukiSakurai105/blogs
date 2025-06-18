from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from models import Post, Comment, Like, Notification, User, Category
from __init__ import db, socketio
from routes.main import create_notification
from forms import CommentForm, PostForm

posts_bp = Blueprint('posts', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@posts_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data, author=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            # Create notification for post author
            if post.author.id != current_user.id:
                create_notification(
                    post.author.id,
                    f"{current_user.username} đã bình luận về bài viết của bạn: {post.title}",
                    url_for('posts.post', post_id=post.id)
                )
            flash('Bình luận của bạn đã được thêm!', 'success')
            return redirect(url_for('posts.post', post_id=post.id))
        else:
            flash('Bạn cần đăng nhập để bình luận.', 'warning')
    return render_template('post.html', post=post, comment_form=form)

@posts_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash('Bạn đã bỏ thích bài viết này!', 'info')
    else:
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        # Create notification for post author
        if post.author.id != current_user.id:
            create_notification(
                post.author.id,
                f"{current_user.username} đã thích bài viết của bạn: {post.title}",
                url_for('posts.post', post_id=post.id)
            )
        flash('Bạn đã thích bài viết này!', 'success')
    return redirect(url_for('posts.post', post_id=post.id))

@posts_bp.route('/post/<int:post_id>/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        flash('Bạn không có quyền xóa bình luận này!', 'danger')
        return redirect(url_for('posts.post', post_id=post_id))
    
    db.session.delete(comment)
    db.session.commit()
    flash('Bình luận đã được xóa!', 'success')
    return redirect(url_for('posts.post', post_id=post_id))

@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        image = form.image.data
        category_id = form.category.data
        post = Post(title=title, content=content, author=current_user, category_id=category_id)
        if image and image.filename != '':
            if not allowed_file(image.filename):
                flash('Chỉ cho phép các tệp hình ảnh!', 'danger')
                return redirect(url_for('posts.create'))
            filename = secure_filename(image.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post.image_path = filename
        db.session.add(post)
        db.session.commit()
        flash('Bài viết đã được tạo thành công!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create.html', form=form)

@posts_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('Bạn không thể chỉnh sửa bài viết này!', 'danger')
        return redirect(url_for('posts.post', post_id=post.id))
    
    form = PostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category_id if post.category_id else None
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.category.data
        image = form.image.data
        post.is_edited = True
        post.edited_at = datetime.now()

        if image and image.filename != '':
            if not allowed_file(image.filename):
                flash('Chỉ cho phép các tệp hình ảnh cho ảnh bài viết!', 'danger')
                return redirect(url_for('posts.edit_post', post_id=post.id))

            if len(image.read()) > current_app.config['MAX_CONTENT_LENGTH']:
                flash('Kích thước ảnh bài viết vượt quá giới hạn 16MB!', 'danger')
                return redirect(url_for('posts.edit_post', post_id=post.id))
            image.seek(0) # Reset stream position after reading size

            filename = secure_filename(image.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            image.save(image_path)
            post.image_path = filename

        db.session.commit()
        flash('Bài viết của bạn đã được cập nhật!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    
    return render_template('edit.html', post=post, form=form)

@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('Bạn không thể xóa bài viết này!', 'danger')
        return redirect(url_for('posts.post', post_id=post.id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Bài viết của bạn đã được xóa!', 'success')
    return redirect(url_for('main.home'))

@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if not content:
        flash('Nội dung bình luận không được để trống!', 'danger')
        return redirect(url_for('posts.post', post_id=post.id))
    
    comment = Comment(content=content, author=current_user, post=post)
    db.session.add(comment)
    
    # Tạo thông báo cho chủ bài viết
    if post.author != current_user:
        notification = Notification(
            user=post.author,
            content=f'{current_user.username} đã bình luận bài viết của bạn: {content[:50]}...',
            link=url_for('posts.post', post_id=post.id)
        )
        db.session.add(notification)
        # Gửi thông báo realtime
        socketio.emit('new_notification', {
            'user_id': post.author.id,
            'content': notification.content,
            'link': notification.link,
            'profile_image': current_user.profile_image,
            'username': current_user.username
        })
    
    db.session.commit()
    flash('Bình luận đã được thêm!', 'success')
    return redirect(url_for('posts.post', post_id=post.id))

@posts_bp.route('/comment/<int:comment_id>/edit', methods=['POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        flash('Bạn không có quyền chỉnh sửa bình luận này!', 'danger')
        return redirect(url_for('posts.post', post_id=comment.post.id))
    
    content = request.form.get('content')
    if not content:
        flash('Nội dung bình luận không được để trống!', 'danger')
        return redirect(url_for('posts.post', post_id=comment.post.id))
    
    comment.content = content
    comment.is_edited = True
    db.session.commit()
    
    flash('Bình luận đã được cập nhật!', 'success')
    return redirect(url_for('posts.post', post_id=comment.post.id)) 

@posts_bp.route('/post/<int:post_id>/remove_image', methods=['POST'])
@login_required
def remove_post_image(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return jsonify({'success': False, 'message': 'Bạn không có quyền xóa ảnh bài viết này!'}), 403

    if post.image_path:
        try:
            file_path = os.path.join(current_app.root_path, 'static', 'uploads', post.image_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            post.image_path = None
            db.session.commit()
            return jsonify({'success': True, 'message': 'Ảnh đã được xóa thành công!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Lỗi khi xóa ảnh: {str(e)}'}), 500
    return jsonify({'success': False, 'message': 'Bài viết không có ảnh để xóa!'}), 404 

@posts_bp.route('/category/<int:category_id>')
def category(category_id):
    from flask import request
    page = request.args.get('page', 1, type=int)
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    categories = Category.query.order_by(Category.name).all()
    return render_template('category_posts.html', category=category, posts=posts, categories=categories) 
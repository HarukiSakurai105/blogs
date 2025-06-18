from flask import Blueprint, request, redirect, url_for, flash
from models import NewsletterSubscriber, db

newsletter_bp = Blueprint('newsletter', __name__)

@newsletter_bp.route('/newsletter/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if not email:
        flash('Vui lòng nhập email!', 'danger')
        return redirect(request.referrer or url_for('main.home'))
    # Kiểm tra trùng email
    if NewsletterSubscriber.query.filter_by(email=email).first():
        flash('Email này đã đăng ký nhận bản tin!', 'warning')
        return redirect(request.referrer or url_for('main.home'))
    # Lưu vào DB
    subscriber = NewsletterSubscriber(email=email)
    db.session.add(subscriber)
    db.session.commit()
    flash('Đăng ký nhận bản tin thành công!', 'success')
    return redirect(request.referrer or url_for('main.home')) 
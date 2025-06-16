from __init__ import create_app, db
from models import User
from datetime import datetime

app = create_app()
with app.app_context():
    users = User.query.all()
    for user in users:
        if not user.date_joined:
            user.date_joined = datetime.utcnow()
    db.session.commit()
    print("Đã cập nhật ngày tham gia cho tất cả người dùng!") 
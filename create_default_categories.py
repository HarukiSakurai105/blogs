from models import Category
from __init__ import db, create_app

# Danh sách chủ đề mặc định giống Spiderum
DEFAULT_CATEGORIES = [
    "Quan điểm - Tranh luận",
    "Khoa học - Công nghệ",
    "Tài chính",
    "Fitness",
    "Thinking Out Loud",
    "Movie",
    "Nhiếp ảnh",
    "Giáo dục",
    "Âm nhạc",
    "Góc nhìn thời sự",
    "Yêu",
    "Nấu ăn Ẩm thực",
    "Life style",
    "Người trong muôn nghề",
    "The Brands",
    "Du lịch",
    "Game",
    "Phát triển bản thân",
    "Sáng tác",
    "Lịch sử",
    "Xe máy",
    "Sách",
    "WTF",
    "Chuyện thầm kín",
    "Ô tô",
    "Fashion",
    "Điêu khắc Kiến trúc Mỹ thuật",
    "Sự kiện Spiderum",
    "Thể thao",
    "Tâm lý học"
]

def create_categories():
    app = create_app()
    with app.app_context():
        for name in DEFAULT_CATEGORIES:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name))
        db.session.commit()
        print("Đã thêm các chủ đề mặc định!")

if __name__ == "__main__":
    create_categories() 
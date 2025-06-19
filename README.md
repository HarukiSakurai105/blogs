# Hướng dẫn cài đặt và chạy project

## 1. Cài đặt Python
- Tải và cài Python 3.11 hoặc mới hơn từ https://www.python.org/downloads/

## 2. (Khuyến nghị) Tạo môi trường ảo
Mở terminal/cmd tại thư mục project, chạy:
```bash
python -m venv venv
```
Kích hoạt môi trường ảo:
- Windows:
  ```
  venv\Scripts\activate
  ```
- Mac/Linux:
  ```
  source venv/bin/activate
  ```

## 3. Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
pip install Flask-Migrate flask-socketio
```

## 4. Thêm các chủ đề mặc định
```bash
python create_default_categories.py
```

## 5. Chạy ứng dụng
```bash
python app.py
```

## 6. Mở trình duyệt và truy cập
```
http://localhost:5000
```

---

**Lưu ý:**  
- Nếu gặp lỗi cơ sở dữ liệu (ví dụ: thiếu cột), hãy xóa file `instance/blog.db` rồi chạy lại bước 4 và 5.
- Nếu chưa có Flask CLI, có thể chạy:
  ```bash
  set FLASK_APP=app.py  # Windows
  export FLASK_APP=app.py  # Mac/Linux
  flask db upgrade
  ```

---

## Hướng dẫn sử dụng

1. Đăng ký tài khoản mới
2. Đăng nhập bằng tài khoản vừa tạo
3. Tạo bài viết mới
4. Sửa hoặc xóa bài viết của bạn
5. Xem bài viết của người dùng khác

## Cấu trúc thư mục project

```
blogs/
├── app.py              # File chạy chính của ứng dụng
├── requirements.txt    # Danh sách các thư viện Python cần thiết
├── static/             # Thư mục chứa file tĩnh (CSS, hình ảnh)
├── templates/          # Thư mục chứa các file giao diện HTML
├── instance/
│   └── blog.db         # File cơ sở dữ liệu SQLite
└── ...
```

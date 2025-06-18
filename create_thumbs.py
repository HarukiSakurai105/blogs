from PIL import Image
import os

UPLOAD_FOLDER = 'static/uploads'
THUMB_FOLDER = os.path.join(UPLOAD_FOLDER, 'thumbs')
os.makedirs(THUMB_FOLDER, exist_ok=True)

for filename in os.listdir(UPLOAD_FOLDER):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        src_path = os.path.join(UPLOAD_FOLDER, filename)
        thumb_path = os.path.join(THUMB_FOLDER, f'thumb_{filename}')
        if not os.path.exists(thumb_path):
            try:
                img = Image.open(src_path)
                img.thumbnail((300, 200))
                img.save(thumb_path)
                print(f"Created thumbnail for {filename}")
            except Exception as e:
                print(f"Error with {filename}: {e}") 
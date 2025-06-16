from PIL import Image, ImageDraw
import os

def create_default_profile():
    # Create a 200x200 image with a light gray background
    img = Image.new('RGB', (200, 200), color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Draw a circle in the center
    draw.ellipse((50, 50, 150, 150), fill='#cccccc')
    
    # Draw a person silhouette
    draw.ellipse((75, 60, 125, 110), fill='#999999')  # Head
    draw.rectangle((90, 110, 110, 160), fill='#999999')  # Body
    
    # Ensure the uploads directory exists
    os.makedirs('static/uploads', exist_ok=True)
    
    # Save the image
    img.save('static/uploads/default_profile.jpg')
    print("Default profile image created successfully!")

if __name__ == '__main__':
    create_default_profile() 
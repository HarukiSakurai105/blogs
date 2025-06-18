from __init__ import create_app, db
from models import User
from datetime import datetime

def update_existing_users():
    app = create_app()
    with app.app_context():
        # Get all users without date_joined
        users_without_date = User.query.filter_by(date_joined=None).all()
        
        if users_without_date:
            print(f"Found {len(users_without_date)} users without date_joined")
            
            # Set a default date for existing users (e.g., now)
            default_date = datetime.utcnow()
            
            for user in users_without_date:
                user.date_joined = default_date
                print(f"Updated user: {user.username}")
            
            db.session.commit()
            print("Successfully updated all users without date_joined")
        else:
            print("All users already have date_joined set")

if __name__ == "__main__":
    update_existing_users() 
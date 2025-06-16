
11. Install the required packages:
```bash
pip install -r requirements.txt
pip install Flask-Migrate
pip install flask-socketio
```
2. Run the application:
```bash
python app.py
```

3. Open your web browser and navigate to:
````
http://localhost:5000
```

## Usage

1. Register a new account
2. Log in with your credentials
3. Create new blog posts
4. Edit or delete your posts
5. View other users' posts

## Project Structure

```
family-blog/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, images)
│   └── style.css      # Custom styles
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── home.html      # Home page
│   ├── about.html     # About page
│   ├── login.html     # Login page
│   ├── register.html  # Registration page
│   ├── create.html    # Create post page
│   └── post.html      # Individual post page
└── instance/          # Instance-specific files
    └── blog.db        # SQLite database
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
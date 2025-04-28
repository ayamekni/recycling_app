from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import json
from io import BytesIO
import base64
import numpy as np
import cv2  # For image processing
import uuid

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after db initialization to avoid circular imports
from models.user import User
from models.bottle import BottleScan

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes
from routes.auth import auth_bp
from routes.bottle import bottle_bp
from routes.dashboard import dashboard_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(bottle_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def index():
    # Get eco-friendly articles (this would typically come from a database or API)
    articles = [
        {
            'title': 'The Impact of Plastic Recycling on Environment',
            'url': 'https://example.com/article1',
            'summary': 'Learn how plastic recycling can reduce landfill waste by up to 80%.'
        },
        {
            'title': 'How Bottle Recycling Saves Energy',
            'url': 'https://example.com/article2',
            'summary': 'Recycling one plastic bottle can save enough energy to power a light bulb for 3 hours.'
        },
        {
            'title': 'The Future of Recycling Technology',
            'url': 'https://example.com/article3',
            'summary': 'Discover how AI and machine learning are revolutionizing recycling processes.'
        }
    ]
    
    # Inspirational quotes about recycling
    quotes = [
        {"text": "There is no such thing as 'away'. When we throw anything away it must go somewhere.", "author": "Annie Leonard"},
        {"text": "The greatest threat to our planet is the belief that someone else will save it.", "author": "Robert Swan"},
        {"text": "Recycling one aluminum can saves enough energy to run a TV for three hours.", "author": "Environmental Protection Agency"}
    ]
    
    return render_template('index.html', articles=articles, quotes=quotes)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
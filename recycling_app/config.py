import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_replace_in_production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # AI Model Configuration
    MODEL_PATH = os.environ.get('MODEL_PATH', 'services/bottle_detection_model.h5')
    
    # Google Maps API Key (for location services)
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
    
    # Recycling Points Data (would typically come from a database)
    RECYCLING_POINTS = [
        {"name": "Green Recycling Center", "lat": 48.8584, "lng": 2.2945, "address": "123 Green St"},
        {"name": "Eco Recycling Hub", "lat": 48.8606, "lng": 2.3376, "address": "456 Eco Ave"},
        {"name": "Planet Savers", "lat": 48.8737, "lng": 2.2950, "address": "789 Planet Rd"}
    ]
    
    # Reward System Configuration
    POINTS_PER_BOTTLE = 10
    REWARD_THRESHOLD = 100  # Points needed for a reward
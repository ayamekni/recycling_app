from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_points = db.Column(db.Integer, default=0)
    total_bottles = db.Column(db.Integer, default=0)
    rewards_claimed = db.Column(db.Integer, default=0)
    
    # Relationship with bottle scans
    bottle_scans = db.relationship('BottleScan', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_points(self, points):
        self.total_points += points
        
    def add_bottle(self):
        self.total_bottles += 1
        
    def claim_reward(self):
        if self.total_points >= 100:  # Assuming 100 points needed for a reward
            self.total_points -= 100
            self.rewards_claimed += 1
            return True
        return False
    
    def get_weekly_stats(self):
        # Get bottle scans for the last 7 days
        now = datetime.utcnow()
        week_ago = now - datetime.timedelta(days=7)
        
        # Group by day and count
        stats = {}
        for i in range(7):
            day = now - datetime.timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            count = self.bottle_scans.filter(
                db.func.date(BottleScan.created_at) == day_str
            ).count()
            stats[day_str] = count
            
        return stats
    
    def __repr__(self):
        return f'<User {self.username}>'
from datetime import datetime
from app import db

class BottleScan(db.Model):
    __tablename__ = 'bottle_scans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_path = db.Column(db.String(255))
    is_recyclable = db.Column(db.Boolean, default=False)
    material_type = db.Column(db.String(50))  # e.g., 'PET', 'HDPE', 'Glass', etc.
    estimated_value = db.Column(db.Float)  # Monetary value
    points_earned = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id, image_path, is_recyclable, material_type, estimated_value):
        self.user_id = user_id
        self.image_path = image_path
        self.is_recyclable = is_recyclable
        self.material_type = material_type
        self.estimated_value = estimated_value
        
        # Calculate points based on material type and recyclability
        if is_recyclable:
            points_map = {
                'PET': 10,
                'HDPE': 12,
                'Glass': 15,
                'Aluminum': 20,
                'Other': 5
            }
            self.points_earned = points_map.get(material_type, 10)
        else:
            self.points_earned = 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_path': self.image_path,
            'is_recyclable': self.is_recyclable,
            'material_type': self.material_type,
            'estimated_value': self.estimated_value,
            'points_earned': self.points_earned,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<BottleScan {self.id} - {self.material_type}>'
"""
Campaign model - C2 campaigns
"""
from datetime import datetime
from . import db


class Campaign(db.Model):
    """C2 campaign for organizing operations"""
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    template = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    commands = db.relationship('Command', backref='campaign', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'template': self.template,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'command_count': len(self.commands)
        }

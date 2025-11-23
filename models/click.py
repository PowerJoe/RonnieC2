"""
Click model - track notification clicks
"""
from datetime import datetime
from . import db


class Click(db.Model):
    """Track notification clicks for analytics"""
    __tablename__ = 'clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    command_id = db.Column(db.Integer, db.ForeignKey('commands.id'), nullable=True)
    
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(512))

"""
Command model - commands sent to agents
"""
from datetime import datetime
from . import db


class Command(db.Model):
    """Commands sent to agents via push notifications"""
    __tablename__ = 'commands'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=True)
    
    command_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    url = db.Column(db.String(500))
    icon = db.Column(db.String(500))
    
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivered = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'campaign_id': self.campaign_id,
            'command_type': self.command_type,
            'title': self.title,
            'message': self.message,
            'url': self.url,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered': self.delivered,
            'clicked': self.clicked
        }

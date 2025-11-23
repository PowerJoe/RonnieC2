"""
Enhanced Fingerprint model - detailed system information
"""
from datetime import datetime
from . import db


class EnhancedFingerprint(db.Model):
    """Enhanced fingerprinting data for agents"""
    __tablename__ = 'enhanced_fingerprints'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    
    # WebGL Fingerprint
    webgl_vendor = db.Column(db.String(200))
    webgl_renderer = db.Column(db.String(200))
    
    # Canvas Fingerprint
    canvas_hash = db.Column(db.String(64))
    
    # Audio Fingerprint
    audio_hash = db.Column(db.String(64))
    
    # Fonts
    fonts_detected = db.Column(db.Text)  # JSON array
    
    # Media Devices
    has_webcam = db.Column(db.Boolean, default=False)
    has_microphone = db.Column(db.Boolean, default=False)
    media_devices_count = db.Column(db.Integer, default=0)
    
    # Battery
    battery_level = db.Column(db.Float)
    battery_charging = db.Column(db.Boolean)
    
    # Network
    network_type = db.Column(db.String(50))
    network_downlink = db.Column(db.Float)
    network_rtt = db.Column(db.Integer)
    
    # Memory
    device_memory_gb = db.Column(db.Integer)
    js_heap_size_mb = db.Column(db.Float)
    
    # Storage
    storage_quota_gb = db.Column(db.Float)
    storage_usage_gb = db.Column(db.Float)
    
    # Additional data
    platform = db.Column(db.String(100))
    cpu_cores = db.Column(db.Integer)
    touch_support = db.Column(db.Boolean)
    
    # Timestamps
    collected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'webgl_vendor': self.webgl_vendor,
            'webgl_renderer': self.webgl_renderer,
            'canvas_hash': self.canvas_hash,
            'audio_hash': self.audio_hash,
            'fonts_detected': self.fonts_detected,
            'has_webcam': self.has_webcam,
            'has_microphone': self.has_microphone,
            'media_devices_count': self.media_devices_count,
            'battery_level': self.battery_level,
            'battery_charging': self.battery_charging,
            'network_type': self.network_type,
            'network_downlink': self.network_downlink,
            'network_rtt': self.network_rtt,
            'device_memory_gb': self.device_memory_gb,
            'js_heap_size_mb': self.js_heap_size_mb,
            'storage_quota_gb': self.storage_quota_gb,
            'storage_usage_gb': self.storage_usage_gb,
            'platform': self.platform,
            'cpu_cores': self.cpu_cores,
            'touch_support': self.touch_support,
            'collected_at': self.collected_at.isoformat() if self.collected_at else None
        }

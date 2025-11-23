"""
Enhanced fingerprinting feature
"""
from flask import Blueprint, request, jsonify
from models import db, Agent, EnhancedFingerprint
import json

fingerprint_bp = Blueprint('fingerprint', __name__)


@fingerprint_bp.route('/fingerprint', methods=['POST'])
def collect_fingerprint():
    """
    Collect enhanced fingerprint data from agent
    
    Expected payload:
    {
        "agent_id": "abc123",
        "webgl": {...},
        "canvas": {...},
        "audio": {...},
        "fonts": [...],
        "media": {...},
        "battery": {...},
        "network": {...},
        "memory": {...},
        "storage": {...}
    }
    """
    try:
        data = request.json
        agent_id = data.get('agent_id')
        
        if not agent_id:
            return jsonify({'error': 'No agent_id provided'}), 400
        
        # Find agent
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        # Extract fingerprint data
        webgl = data.get('webgl', {})
        canvas = data.get('canvas', {})
        audio = data.get('audio', {})
        fonts = data.get('fonts', [])
        media = data.get('media', {})
        battery = data.get('battery', {})
        network = data.get('network', {})
        memory = data.get('memory', {})
        storage = data.get('storage', {})
        system = data.get('system', {})
        
        # Create enhanced fingerprint record
        fingerprint = EnhancedFingerprint(
            agent_id=agent.id,
            
            # WebGL
            webgl_vendor=webgl.get('vendor'),
            webgl_renderer=webgl.get('renderer'),
            
            # Canvas
            canvas_hash=canvas.get('hash'),
            
            # Audio
            audio_hash=audio.get('hash'),
            
            # Fonts
            fonts_detected=json.dumps(fonts),
            
            # Media devices
            has_webcam=media.get('hasWebcam', False),
            has_microphone=media.get('hasMicrophone', False),
            media_devices_count=media.get('deviceCount', 0),
            
            # Battery
            battery_level=battery.get('level'),
            battery_charging=battery.get('charging'),
            
            # Network
            network_type=network.get('type'),
            network_downlink=network.get('downlink'),
            network_rtt=network.get('rtt'),
            
            # Memory
            device_memory_gb=memory.get('deviceMemory'),
            js_heap_size_mb=memory.get('jsHeapSize'),
            
            # Storage
            storage_quota_gb=storage.get('quota'),
            storage_usage_gb=storage.get('usage'),
            
            # System
            platform=system.get('platform'),
            cpu_cores=system.get('cpuCores'),
            touch_support=system.get('touchSupport')
        )
        
        db.session.add(fingerprint)
        db.session.commit()
        
        print(f"[+] Enhanced fingerprint collected from agent {agent_id}")
        print(f"    WebGL: {webgl.get('renderer')}")
        print(f"    Media: {media.get('deviceCount')} devices")
        print(f"    Fonts: {len(fonts)} detected")
        
        return jsonify({
            'success': True,
            'message': 'Fingerprint collected',
            'fingerprint_id': fingerprint.id
        })
        
    except Exception as e:
        print(f"[-] Fingerprint collection error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@fingerprint_bp.route('/fingerprints/<int:agent_id>', methods=['GET'])
def get_agent_fingerprints(agent_id):
    """Get all fingerprints for an agent"""
    fingerprints = EnhancedFingerprint.query.filter_by(agent_id=agent_id)\
        .order_by(EnhancedFingerprint.collected_at.desc())\
        .all()
    
    return jsonify([fp.to_dict() for fp in fingerprints])

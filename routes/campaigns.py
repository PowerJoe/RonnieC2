"""
Campaign management routes
"""
from flask import Blueprint, request, jsonify
from models import db, Campaign

campaigns_bp = Blueprint('campaigns', __name__)


@campaigns_bp.route('/campaigns', methods=['GET', 'POST'])
def campaigns():
    """Manage campaigns"""
    if request.method == 'GET':
        campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
        return jsonify([c.to_dict() for c in campaigns])
    
    elif request.method == 'POST':
        data = request.json
        campaign = Campaign(
            name=data.get('name'),
            description=data.get('description'),
            template=data.get('template')
        )
        db.session.add(campaign)
        db.session.commit()
        
        return jsonify(campaign.to_dict()), 201

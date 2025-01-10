import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from flask import Flask, request
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
    app.config['JWT_COOKIE_SECURE'] = is_production
    app.config['JWT_COOKIE_CSRF_PROTECT'] = is_production
    app.config['JWT_COOKIE_SAMESITE'] = 'None' if is_production else 'Lax'
    
    # Configure CORS based on environment
    origins = [
        "http://localhost:5173",  # Development frontend
        "https://universalmatchingv2.web.app",  # Production frontend
        "https://universalmatchingv2.firebaseapp.com",  # Alternative production frontend
        "https://backend-universalmatchingv2-uc.a.run.app"  # Cloud Run backend
    ]
    
    # Enable CORS with cookie support
    CORS(app, 
         resources={r"/api/*": {
             "origins": origins,
             "supports_credentials": True,
             "allow_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "expose_headers": ["Set-Cookie"],
             "allow_credentials": True  # Important for cookies
         }})

    # Add CORS headers to all responses
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin in origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Expose-Headers'] = 'Set-Cookie'
            
            # Add SameSite attribute for cookies in production
            if is_production and 'Set-Cookie' in response.headers:
                response.headers['Set-Cookie'] = response.headers['Set-Cookie'].split(';')[0] + '; SameSite=None; Secure'
        return response

    jwt = JWTManager(app)

    # Register blueprints
    from apps.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 
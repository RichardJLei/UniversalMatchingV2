import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import logging
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv
import os
from google.cloud import error_reporting

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    load_dotenv()
    logger.info("Environment variables loaded")
except Exception as e:
    logger.error(f"Error loading environment variables: {str(e)}")
    traceback.print_exc()

def create_app():
    """Application factory function"""
    try:
        app = Flask(__name__)
        
        # Initialize error reporting
        error_client = error_reporting.Client()
        
        # Log startup information
        logger.info("Starting application...")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Files in current directory: {os.listdir('.')}")
        
        # Determine environment
        is_production = os.environ.get('FLASK_ENV') == 'production'
        logger.info(f"Environment: {'production' if is_production else 'development'}")
        
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
            logger.info({
                "message": "Request details",
                "origin": origin,
                "method": request.method,
                "headers": dict(request.headers)
            })
            
            if origin in origins:
                logger.info(f"Origin {origin} is allowed")
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response.headers['Access-Control-Expose-Headers'] = 'Set-Cookie'
                
                if is_production and 'Set-Cookie' in response.headers:
                    response.headers['Set-Cookie'] = response.headers['Set-Cookie'].split(';')[0] + '; SameSite=None; Secure'
                    
                print("Response Headers:", dict(response.headers))
            else:
                logger.warning({
                    "message": "Origin not allowed",
                    "origin": origin,
                    "allowed_origins": origins
                })
                
            return response

        @app.errorhandler(Exception)
        def handle_error(error):
            error_client.report_exception()
            logger.error(f"Unhandled error: {str(error)}", exc_info=True)
            return jsonify({'error': str(error)}), 500

        jwt = JWTManager(app)

        # Register blueprints
        from apps.auth.routes import auth_bp
        app.register_blueprint(auth_bp)

        # Print environment variables (excluding sensitive ones)
        print("\n=== Environment Variables ===")
        for key, value in os.environ.items():
            if not any(sensitive in key.lower() for sensitive in ['key', 'secret', 'password', 'token']):
                print(f"{key}: {value}")

        return app
    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        traceback.print_exc()
        raise

# Create the application instance
application = create_app()

# For local development
if __name__ == '__main__':
    application.run(debug=True)

# For Gunicorn
app = application 
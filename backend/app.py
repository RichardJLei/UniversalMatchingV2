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

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Explicitly log to stdout
    ]
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
        CORS(app, resources={
            r"/api/*": {
                "origins": [
                    "https://universalmatchingv2.web.app",
                    "https://universalmatchingv2.firebaseapp.com",
                    "https://universalmatchingv2-181579031870.asia-southeast1.run.app",  # Add backend URL
                    "http://localhost:5173"  # For local development
                ],
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "expose_headers": ["Set-Cookie", "Access-Control-Allow-Credentials"]
            }
        })

        # Add CORS headers to all responses
        @app.after_request
        def after_request(response):
            origin = request.headers.get('Origin')
            logger.info(f"Handling request from origin: {origin}")
            
            if origin in origins:
                logger.info("Setting CORS headers for allowed origin")
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response.headers['Access-Control-Expose-Headers'] = 'Set-Cookie'
                
                if is_production and 'Set-Cookie' in response.headers:
                    logger.info("Setting secure cookie headers for production")
                    response.headers['Set-Cookie'] = response.headers['Set-Cookie'].split(';')[0] + '; SameSite=None; Secure'
            else:
                logger.warning(f"Request from unauthorized origin: {origin}")
            
            logger.info({
                "message": "Response details",
                "origin": origin,
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "headers": dict(response.headers)
            })
            
            return response

        @app.errorhandler(Exception)
        def handle_error(error):
            logger.error(f"Unhandled error: {str(error)}", exc_info=True)
            return jsonify({'error': str(error)}), 500

        jwt = JWTManager(app)

        # Register blueprints
        from apps.auth.routes import auth_bp
        app.register_blueprint(auth_bp)

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
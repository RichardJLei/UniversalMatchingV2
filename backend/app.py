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
from werkzeug.exceptions import HTTPException

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
        allowed_origins = [
            "http://localhost:5173",  # Your local frontend
            "https://universalmatchingv2.web.app",
            "https://universalmatchingv2.firebaseapp.com",
            "https://universalmatchingv2-181579031870.asia-southeast1.run.app"
        ]
        
        CORS(app, resources={
            r"/*": {
                "origins": allowed_origins,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "expose_headers": ["Set-Cookie", "Access-Control-Allow-Credentials"]
            }
        })

        # Add CORS headers to all responses
        @app.after_request
        def after_request(response):
            origin = request.headers.get('Origin')
            
            # Only process CORS for actual origins (not None or empty)
            if origin and origin in allowed_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response.headers['Access-Control-Expose-Headers'] = 'Set-Cookie'
                
                if is_production and 'Set-Cookie' in response.headers:
                    cookie_parts = response.headers['Set-Cookie'].split(';')[0]
                    response.headers['Set-Cookie'] = f"{cookie_parts}; SameSite=None; Secure"
            
            # Log response details for debugging
            logger.debug({
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
            status_code = getattr(error, 'code', 500)
            
            # Log the full error details
            logger.error(f"Error handling request: {str(error)}", exc_info=True)
            logger.error(f"Request details - Method: {request.method}, Path: {request.path}, Headers: {dict(request.headers)}")
            
            error_response = {
                'error': str(error),
                'status_code': status_code,
                'path': request.path,
                'method': request.method
            }
            
            if not isinstance(error, HTTPException):
                status_code = 500
                error_response['error'] = 'Internal Server Error'
            
            response = jsonify(error_response)
            
            # Handle CORS for error responses
            origin = request.headers.get('Origin')
            if origin and origin in allowed_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                if request.method == 'OPTIONS':
                    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                    response.headers['Access-Control-Max-Age'] = '3600'
                    status_code = 200  # Return 200 for OPTIONS requests
            
            return response, status_code

        jwt = JWTManager(app)

        # Register blueprints with proper URL prefix
        from apps.auth.routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')

        # Add health check route with minimal processing
        @app.route('/', methods=['GET'])
        def root():
            return jsonify({
                'status': 'healthy',
                'service': 'Universal Matching API',
                'version': '1.0'
            }), 200  # Explicitly return 200 status

        @app.route('/api/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy'}), 200

        # Add OPTIONS handler for CORS preflight requests
        @app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
        @app.route('/<path:path>', methods=['OPTIONS'])
        def handle_options(path):
            response = app.make_default_options_response()
            origin = request.headers.get('Origin')
            
            if origin in allowed_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Max-Age'] = '3600'
            
            return response

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
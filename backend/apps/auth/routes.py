from flask import Blueprint, jsonify, request, current_app
from services.factory import get_auth_service, get_database_service
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from firebase_admin import auth as firebase_auth
import time
import os
import logging

auth_bp = Blueprint('auth', __name__)
auth_service = get_auth_service()
db_service = get_database_service()
logger = logging.getLogger(__name__)

@auth_bp.route('/validate', methods=['POST', 'OPTIONS'])
def validate_token():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
            
        token = auth_header.split('Bearer ')[1]
        if not token:
            return jsonify({'error': 'Invalid token format'}), 401

        try:
            decoded_token = auth_service.verify_token(token)
            if decoded_token:
                logger.info(f"Token validated for user: {decoded_token.get('email')}")
                return jsonify({'status': 'success', 'user': decoded_token})
            else:
                return jsonify({'error': 'Invalid token'}), 401

        except Exception as e:
            logger.error(f"Token validation error: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 401

    except Exception as e:
        logger.error(f"Validation route error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    response = jsonify({'message': 'Successfully logged out'})
    unset_jwt_cookies(response)
    return response, 200

@auth_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'auth'
    }), 200 

@auth_bp.route('/health/db', methods=['GET'])
def db_health_check():
    try:
        # Test database connection
        db_service.get_client().admin.command('ping')
        return jsonify({
            'status': 'healthy',
            'service': 'auth',
            'database': 'connected',
            'connection_string': db_service.get_connection_string()[:20] + '...' # Show partial string for security
        }), 200
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'auth',
            'database': 'disconnected',
            'error': str(e)
        }), 500 

@auth_bp.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    allowed_origins = current_app.config.get('CORS_ORIGINS', [
        "http://localhost:5173",
        "https://universalmatchingv2.web.app",
        "https://universalmatchingv2.firebaseapp.com",
        "https://universalmatchingv2-181579031870.asia-southeast1.run.app"
    ])
    
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response 
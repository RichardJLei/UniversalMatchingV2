from flask import Blueprint, jsonify, request
from services.factory import get_auth_service, get_database_service
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from datetime import datetime, timedelta
from firebase_admin import auth as firebase_auth
import time
import os
import logging

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = get_auth_service()
db_service = get_database_service()
logger = logging.getLogger(__name__)

@auth_bp.route('/api/auth/validate', methods=['POST', 'OPTIONS'])
async def validate_token():
    """Validate Firebase token and create session"""
    logger.info(f"\n=== Validate Token Request ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Origin: {request.headers.get('Origin')}")
    
    # Handle preflight request
    if request.method == 'OPTIONS':
        logger.info("Handling OPTIONS request")
        response = jsonify({'message': 'OK'})
        origin = request.headers.get('Origin')
        
        logger.info(f"Setting CORS headers for origin: {origin}")
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        logger.info("Response Headers:", dict(response.headers))
        return response

    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        logger.info(f"Auth header: {auth_header[:20]}...")  # Print first 20 chars for security
        
        if not auth_header.startswith('Bearer '):
            logger.warning("No Bearer token found")
            return jsonify({'error': 'No token provided'}), 401
            
        token = auth_header.split('Bearer ')[1]
        if not token:
            logger.warning("Empty token after Bearer")
            return jsonify({'error': 'Invalid token format'}), 401

        try:
            decoded_token = auth_service.verify_token(token)
            if decoded_token:
                logger.info(f"Token validated for user: {decoded_token.get('email')}")
                return jsonify({'status': 'success', 'user': decoded_token})
            else:
                logger.warning("Token validation failed")
                return jsonify({'error': 'Invalid token'}), 401

        except Exception as e:
            logger.error(f"Token validation error: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 401

    except Exception as e:
        logger.error(f"Validation route error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/logout', methods=['POST', 'OPTIONS'])
def logout():
    """Clear session cookies"""
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'OK'})
        return response

    try:
        response = jsonify({'message': 'Logged out successfully'})
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Failed to logout'}), 500

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
    if origin in app.config['CORS_ORIGINS']:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response 
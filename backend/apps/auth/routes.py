from flask import Blueprint, jsonify, request
from services.factory import get_auth_service
from flask_jwt_extended import create_access_token, set_access_cookies

auth_bp = Blueprint('auth', __name__)
auth_service = get_auth_service()

@auth_bp.route('/api/auth/validate', methods=['POST'])
async def validate_token():
    """Validate Firebase token and create session"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_info = await auth_service.verify_token(token)
        
        if not user_info:
            return jsonify({'error': 'Invalid token'}), 401

        # Create session token
        access_token = create_access_token(identity=user_info['user_id'])
        response = jsonify(user_info)
        set_access_cookies(response, access_token)
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
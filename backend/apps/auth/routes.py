from flask import Blueprint, jsonify, request
from services.factory import get_auth_service, get_database_service
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from datetime import datetime

auth_bp = Blueprint('auth', __name__)
auth_service = get_auth_service()
db_service = get_database_service()

@auth_bp.route('/api/auth/validate', methods=['POST'])
async def validate_token():
    """Validate Firebase token and create session"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_info = auth_service.verify_token(token)
        
        if not user_info:
            return jsonify({'error': 'Invalid token'}), 401

        # Check if user exists in database
        existing_user = await db_service.find_user_by_email(user_info['email'])
        
        if not existing_user:
            # Create new user with default role
            user_data = {
                'firebase_uid': user_info['user_id'],
                'email': user_info['email'],
                'name': user_info.get('name'),
                'photo_url': user_info.get('picture'),
                'role': 'user',
                'created_at': datetime.utcnow(),
                'last_login': datetime.utcnow()
            }
            await db_service.create_user(user_data)
        else:
            # Update last login time
            await db_service.update_one(
                'users',
                {'email': user_info['email']},
                {'last_login': datetime.utcnow()}
            )

        # Create session
        access_token = create_access_token(identity=user_info['user_id'])
        response = jsonify(user_info)
        set_access_cookies(response, access_token)
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Clear session cookies"""
    response = jsonify({'message': 'Logged out successfully'})
    unset_jwt_cookies(response)
    return response 
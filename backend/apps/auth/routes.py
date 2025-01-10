from flask import Blueprint, jsonify, request
from services.factory import get_auth_service, get_database_service
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from datetime import datetime, timedelta
from firebase_admin import auth as firebase_auth
import time
import os

auth_bp = Blueprint('auth', __name__)
auth_service = get_auth_service()
db_service = get_database_service()

@auth_bp.route('/api/auth/validate', methods=['POST', 'OPTIONS'])
async def validate_token():
    """Validate Firebase token and create session"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'OK'})
        # Add all required CORS headers for preflight
        origin = request.headers.get('Origin')
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
            
        token = auth_header.split('Bearer ')[1]
        if not token:
            return jsonify({'error': 'Invalid token format'}), 401

        # Add a small delay to handle clock skew
        time.sleep(1)

        try:
            decoded_token = firebase_auth.verify_id_token(
                token,
                check_revoked=True
            )
            user_info = {
                'user_id': decoded_token['uid'],
                'email': decoded_token.get('email'),
                'name': decoded_token.get('name'),
                'picture': decoded_token.get('picture')
            }
        except firebase_auth.InvalidIdTokenError as e:
            if "Token used too early" in str(e):
                time.sleep(1)
                try:
                    decoded_token = firebase_auth.verify_id_token(token, check_revoked=True)
                    user_info = {
                        'user_id': decoded_token['uid'],
                        'email': decoded_token.get('email'),
                        'name': decoded_token.get('name'),
                        'picture': decoded_token.get('picture')
                    }
                except Exception as retry_error:
                    print(f"Retry token validation error: {str(retry_error)}")
                    return jsonify({'error': 'Invalid token after retry'}), 401
            else:
                print(f"Token validation error: {str(e)}")
                return jsonify({'error': 'Invalid token'}), 401

        if not user_info:
            return jsonify({'error': 'Invalid token'}), 401

        try:
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
            response = jsonify({
                'status': 'success',
                'user': user_info
            })
            set_access_cookies(response, access_token)
            
            # Set SameSite attribute for cookies in production
            is_production = os.environ.get('FLASK_ENV') == 'production'
            if is_production and 'Set-Cookie' in response.headers:
                response.headers['Set-Cookie'] = response.headers['Set-Cookie'].split(';')[0] + '; SameSite=None; Secure'
            
            return response

        except Exception as db_error:
            print(f"Database error: {str(db_error)}")
            # Still return success even if DB operations fail
            return jsonify({'status': 'success', 'user': user_info})

    except Exception as e:
        print(f"Token validation error: {str(e)}")
        return jsonify({'error': str(e)}), 401

@auth_bp.route('/api/auth/logout', methods=['POST', 'OPTIONS'])
def logout():
    """Clear session cookies"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'OK'})
        # Add all required CORS headers for preflight
        origin = request.headers.get('Origin')
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    try:
        response = jsonify({'message': 'Logged out successfully'})
        unset_jwt_cookies(response)
        
        # Set SameSite attribute for cookies
        is_production = os.environ.get('FLASK_ENV') == 'production'
        if is_production and 'Set-Cookie' in response.headers:
            response.headers['Set-Cookie'] = response.headers['Set-Cookie'].split(';')[0] + '; SameSite=None; Secure'
            
        return response
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return jsonify({'error': 'Failed to logout'}), 500 
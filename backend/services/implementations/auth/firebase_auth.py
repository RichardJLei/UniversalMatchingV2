from typing import Optional, Dict
import firebase_admin
from firebase_admin import auth, credentials
from ...interfaces.auth import AuthService
from config.config import Config

class FirebaseAuthService(AuthService):
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        try:
            firebase_admin.get_app()
        except ValueError:
            config = Config()
            cred = credentials.Certificate(config.AUTH_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify Firebase ID token"""
        try:
            if not token:
                return None
                
            decoded_token = auth.verify_id_token(token)
            return {
                'user_id': decoded_token['uid'],
                'email': decoded_token.get('email'),
                'name': decoded_token.get('name'),
                'picture': decoded_token.get('picture')
            }
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return None

    async def create_user(self, email: str, password: str) -> Dict:
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return {
                "id": user.uid,
                "email": user.email,
                "email_verified": user.email_verified
            }
        except auth.EmailAlreadyExistsError:
            raise ValueError("Email already exists")
        except ValueError as e:
            error_msg = str(e)
            # Handle specific Firebase validation errors
            if "Malformed email address" in error_msg:
                raise ValueError("Invalid email")
            elif "Invalid password string" in error_msg or "Password must be" in error_msg:
                raise ValueError("Invalid password")
            else:
                raise ValueError(str(e))
        except exceptions.FirebaseError as e:
            # Handle other Firebase-specific errors
            if "INVALID_ARGUMENT" in str(e):
                raise ValueError("Invalid input")
            elif "PERMISSION_DENIED" in str(e):
                raise ValueError("Permission denied")
            else:
                raise ValueError(f"Firebase error: {str(e)}") 
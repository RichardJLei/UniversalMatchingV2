from typing import Optional, Dict
import firebase_admin
from firebase_admin import auth, exceptions
from ...interfaces.auth import AuthService

class FirebaseAuthService(AuthService):
    def __init__(self):
        if not firebase_admin._apps:
            firebase_admin.initialize_app()

    async def verify_token(self, token: str) -> Optional[Dict]:
        try:
            decoded_token = auth.verify_id_token(token)
            return {
                "user_id": decoded_token["uid"],
                "email": decoded_token.get("email"),
                "email_verified": decoded_token.get("email_verified", False)
            }
        except (auth.InvalidIdTokenError, ValueError):
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
from typing import Optional, Dict
import firebase_admin
from firebase_admin import auth
from ...interfaces.auth import AuthService

class FirebaseAuthService(AuthService):
    def __init__(self):
        if not firebase_admin._apps:
            firebase_admin.initialize_app()

    async def verify_token(self, token: str) -> Optional[Dict]:
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except:
            return None

    async def create_user(self, email: str, password: str) -> Dict:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user.__dict__ 
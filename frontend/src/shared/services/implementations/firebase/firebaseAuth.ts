import { initializeApp } from 'firebase/app'
import { 
  getAuth, 
  signInWithPopup, 
  GoogleAuthProvider,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User as FirebaseUser
} from 'firebase/auth'
import { AuthService, User } from '../../interfaces/auth'

// Initialize Firebase with environment variables
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID
};

// Initialize Firebase only once
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export class FirebaseAuthService implements AuthService {
  private provider = new GoogleAuthProvider();

  private async validateWithBackend(firebaseUser: FirebaseUser): Promise<void> {
    const token = await firebaseUser.getIdToken();
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/auth/validate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      credentials: 'include'
    });

    if (!response.ok) {
      throw new Error('Failed to validate with backend');
    }
  }

  async signInWithGoogle(): Promise<User> {
    try {
      const result = await signInWithPopup(auth, this.provider);
      await this.validateWithBackend(result.user);
      
      return {
        id: result.user.uid,
        email: result.user.email!,
        name: result.user.displayName,
        photoURL: result.user.photoURL,
        lastLogin: new Date(result.user.metadata.lastSignInTime!)
      };
    } catch (error) {
      console.error('Error signing in with Google:', error);
      throw new Error('Failed to sign in with Google');
    }
  }

  async signOut(): Promise<void> {
    try {
      await firebaseSignOut(auth)
    } catch (error) {
      console.error('Error signing out:', error)
      throw new Error('Failed to sign out')
    }
  }

  async getCurrentUser(): Promise<User | null> {
    return new Promise((resolve) => {
      onAuthStateChanged(auth, (user) => {
        resolve(user ? {
          id: user.uid,
          email: user.email!,
          name: user.displayName,
          photoURL: user.photoURL,
          lastLogin: new Date(user.metadata.lastSignInTime!)
        } : null)
      })
    })
  }
} 
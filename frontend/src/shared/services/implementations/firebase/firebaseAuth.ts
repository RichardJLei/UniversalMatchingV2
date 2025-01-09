import { initializeApp } from 'firebase/app'
import { 
  getAuth, 
  signInWithPopup, 
  GoogleAuthProvider,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User as FirebaseUser,
  browserLocalPersistence,
  setPersistence
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

// Set persistence once at startup
setPersistence(auth, browserLocalPersistence)
  .catch(error => console.error('Error setting persistence:', error));

export class FirebaseAuthService implements AuthService {
  private provider: GoogleAuthProvider;

  constructor() {
    this.provider = new GoogleAuthProvider();
    // Only set the essential parameter
    this.provider.setCustomParameters({
      prompt: 'select_account'
    });
  }

  private async validateWithBackend(firebaseUser: FirebaseUser): Promise<void> {
    try {
      const token = await firebaseUser.getIdToken();
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/auth/validate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      if (!response.ok) {
        const error = await response.json();
        console.error('Backend validation error:', error);
        // Don't throw error, just log it
        return;
      }
    } catch (error) {
      console.warn('Backend validation failed:', error);
      // Don't throw error, continue with client-side auth
    }
  }

  async signInWithGoogle(): Promise<User | null> {
    try {
      const result = await signInWithPopup(auth, this.provider);
      
      try {
        await this.validateWithBackend(result.user);
      } catch (error) {
        console.warn('Backend validation failed:', error);
      }
      
      return {
        id: result.user.uid,
        email: result.user.email!,
        name: result.user.displayName,
        photoURL: result.user.photoURL,
        lastLogin: new Date(result.user.metadata.lastSignInTime!)
      };
    } catch (error: any) {
      console.error('Error signing in with Google:', error);
      
      if (error.code === 'auth/popup-closed-by-user' || 
          error.code === 'auth/cancelled-popup-request') {
        return null;
      }
      
      throw error;
    }
  }

  async signOut(): Promise<void> {
    try {
      // Clear backend session
      await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      });
      
      // Sign out from Firebase
      await firebaseSignOut(auth);
      
      // Clear local storage
      localStorage.removeItem('user');
    } catch (error) {
      console.error('Error signing out:', error);
      await firebaseSignOut(auth);
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
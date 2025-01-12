import { initializeApp, getApps, deleteApp } from 'firebase/app'
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

// Clear any existing Firebase apps
getApps().forEach(app => {
  deleteApp(app);
});

// Initialize Firebase with environment variables
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID
};

// Initialize Firebase only once
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Force auth settings
auth.useDeviceLanguage();
auth.settings.appVerificationDisabledForTesting = false;

// Set persistence once at startup
setPersistence(auth, browserLocalPersistence)
  .catch(error => console.error('Error setting persistence:', error));

export class FirebaseAuthService implements AuthService {
  private provider: GoogleAuthProvider;

  constructor() {
    this.provider = new GoogleAuthProvider();
    // Only set supported parameters
    this.provider.setCustomParameters({
      prompt: 'select_account',
    });
  }

  private async validateWithBackend(firebaseUser: FirebaseUser): Promise<{ isNewUser: boolean }> {
    try {
        const token = await firebaseUser.getIdToken(true);
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/validate`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Backend validation failed');
        }

        const data = await response.json();
        console.log('Backend validation response:', data); // Debug log
        return { 
            isNewUser: data.is_new_user 
        };
    } catch (error) {
        console.warn('Backend validation failed:', error);
        return { isNewUser: false };
    }
  }

  async signInWithGoogle(): Promise<AuthResponse> {
    try {
        const result = await signInWithPopup(auth, this.provider);
        const { isNewUser } = await this.validateWithBackend(result.user);
        
        console.log('Sign in response - isNewUser:', isNewUser); // Debug log
        
        return {
            user: {
                id: result.user.uid,
                email: result.user.email!,
                name: result.user.displayName,
                photoURL: result.user.photoURL,
                lastLogin: new Date(result.user.metadata.lastSignInTime!)
            },
            isNewUser
        };
    } catch (error: any) {
        console.error('Error signing in with Google:', error);
        if (error.code === 'auth/popup-closed-by-user' || 
            error.code === 'auth/cancelled-popup-request') {
            return {
                user: null,
                isNewUser: false
            };
        }
        throw error;
    }
  }

  async signOut(): Promise<void> {
    try {
      // Clear backend session
      await fetch(`${import.meta.env.VITE_API_URL}/api/auth/logout`, {
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

  async getCurrentUser(): Promise<AuthResponse> {
    return new Promise((resolve) => {
      onAuthStateChanged(auth, (user) => {
        if (user) {
          resolve({
            user: {
              id: user.uid,
              email: user.email!,
              name: user.displayName,
              photoURL: user.photoURL,
              lastLogin: new Date(user.metadata.lastSignInTime!)
            },
            isNewUser: false
          });
        } else {
          resolve({
            user: null,
            isNewUser: false
          });
        }
      });
    });
  }
} 
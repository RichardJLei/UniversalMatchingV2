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

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: `${import.meta.env.VITE_FIREBASE_PROJECT_ID}.appspot.com`,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
}

// Initialize Firebase only once
let app;
try {
  app = initializeApp(firebaseConfig);
} catch (error) {
  // Ignore the duplicate app initialization error
  if (!/already exists/.test(error.message)) {
    console.error('Firebase initialization error', error);
  }
}

export class FirebaseAuthService implements AuthService {
  private auth;
  private provider;

  constructor() {
    this.auth = getAuth(app);
    this.provider = new GoogleAuthProvider();
  }

  private convertUser(firebaseUser: FirebaseUser): User {
    return {
      id: firebaseUser.uid,
      email: firebaseUser.email!,
      name: firebaseUser.displayName,
      photoURL: firebaseUser.photoURL,
      lastLogin: new Date(firebaseUser.metadata.lastSignInTime!)
    }
  }

  async signInWithGoogle(): Promise<User> {
    try {
      const result = await signInWithPopup(this.auth, this.provider)
      return this.convertUser(result.user)
    } catch (error) {
      console.error('Error signing in with Google:', error)
      throw new Error('Failed to sign in with Google')
    }
  }

  async signOut(): Promise<void> {
    try {
      await firebaseSignOut(this.auth)
    } catch (error) {
      console.error('Error signing out:', error)
      throw new Error('Failed to sign out')
    }
  }

  async getCurrentUser(): Promise<User | null> {
    return new Promise((resolve) => {
      onAuthStateChanged(this.auth, (user) => {
        resolve(user ? this.convertUser(user) : null)
      })
    })
  }
} 
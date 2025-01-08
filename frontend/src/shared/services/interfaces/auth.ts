export interface User {
  id: string
  email: string
  name: string | null
  photoURL: string | null
  lastLogin: Date
}

export interface AuthService {
  signInWithGoogle(): Promise<User>
  signOut(): Promise<void>
  getCurrentUser(): Promise<User | null>
} 
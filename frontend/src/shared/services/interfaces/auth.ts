export interface User {
  id: string
  email: string
  name: string | null
  photoURL: string | null
  lastLogin: Date
}

export interface AuthResponse {
  user: User | null
  isNewUser: boolean
}

export interface AuthService {
  getCurrentUser: () => Promise<AuthResponse>
  signInWithGoogle: () => Promise<AuthResponse>
  signOut: () => Promise<void>
} 
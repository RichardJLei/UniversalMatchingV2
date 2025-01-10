import { createContext, useContext, useState, useEffect, FC, ReactNode } from 'react'
import { useNavigate } from 'react-router-dom'
import { User, AuthService } from '../services/interfaces/auth'
import { FirebaseAuthService } from '../services/implementations/firebase/firebaseAuth'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  signIn: () => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const authService: AuthService = new FirebaseAuthService()
  const navigate = useNavigate()

  useEffect(() => {
    const initAuth = async () => {
      try {
        const currentUser = await authService.getCurrentUser()
        setUser(currentUser)
        navigate('/home')
      } catch (error) {
        console.error('Error initializing auth:', error)
      } finally {
        setIsLoading(false)
      }
    }

    initAuth()
  }, [navigate])

  const signIn = async () => {
    try {
      const user = await authService.signInWithGoogle()
      if (user) {
        setUser(user)
        navigate('/home')
      }
    } catch (error: any) {
      console.error('Error signing in:', error)
      throw error
    }
  }

  const signOut = async () => {
    try {
      await authService.signOut()
      setUser(null)
      navigate('/home')
    } catch (error) {
      console.error('Error signing out:', error)
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
} 
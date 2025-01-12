import { createContext, useContext, useState, useEffect, FC, ReactNode, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { User, AuthService } from '../services/interfaces/auth'
import { FirebaseAuthService } from '../services/implementations/firebase/firebaseAuth'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  isNewUser: boolean
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
  const [isNewUser, setIsNewUser] = useState(false)
  const initialRenderRef = useRef(true)
  const authService: AuthService = new FirebaseAuthService()
  const navigate = useNavigate()

  useEffect(() => {
    let isMounted = true;

    const initAuth = async () => {
      try {
        const response = await authService.getCurrentUser();
        if (isMounted) {
          setUser(response.user);
          if (initialRenderRef.current) {
            setIsNewUser(response.isNewUser);
            initialRenderRef.current = false;
          }
          if (response.user) {
            navigate('/home');
          }
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    initAuth();
    return () => {
      isMounted = false;
    };
  }, [navigate]);

  const signIn = async () => {
    try {
      const { user, isNewUser: newUser } = await authService.signInWithGoogle()
      if (user) {
        setUser(user)
        setIsNewUser(newUser)
        console.log('Sign in completed - isNewUser:', newUser)
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
      setIsNewUser(false)
      initialRenderRef.current = true
      navigate('/')
    } catch (error) {
      console.error('Error signing out:', error)
      setUser(null)
      setIsNewUser(false)
    }
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, isNewUser, signIn, signOut }}>
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
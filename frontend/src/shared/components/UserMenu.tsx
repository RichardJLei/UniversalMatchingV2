import { FC } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { LogOut, User } from 'lucide-react'

export const UserMenu: FC = () => {
  const { user, isLoading, signIn, signOut } = useAuth()

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 w-20 bg-gray-200 dark:bg-gray-700 rounded" />
      </div>
    )
  }

  if (!user) {
    return (
      <button 
        onClick={() => signIn()}
        className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 
                   hover:bg-gray-100 dark:hover:bg-gray-800 
                   rounded-md transition-colors"
      >
        Sign in
      </button>
    )
  }

  return (
    <div className="flex items-center gap-4">
      <div className="flex items-center gap-2">
        {user.photoURL ? (
          <img 
            src={user.photoURL} 
            alt={user.name || 'User'} 
            className="w-8 h-8 rounded-full"
          />
        ) : (
          <User className="w-8 h-8 p-1 rounded-full bg-gray-100 dark:bg-gray-800" />
        )}
        <span className="text-sm font-medium text-gray-700 dark:text-gray-200">
          {user.name || user.email}
        </span>
      </div>
      <button
        onClick={() => signOut()}
        className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 
                   dark:hover:text-gray-200 transition-colors"
        aria-label="Sign out"
      >
        <LogOut className="w-5 h-5" />
      </button>
    </div>
  )
} 
import { FC, useState, useRef, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { LogOut, User, ChevronDown } from 'lucide-react'

export const UserMenu: FC = () => {
  const { user, isLoading, signIn, signOut } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

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
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-md 
                   hover:bg-gray-100 dark:hover:bg-gray-800 
                   transition-colors"
      >
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
        <ChevronDown className="w-4 h-4 text-gray-500" />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 py-1 bg-white dark:bg-gray-800 
                      rounded-md shadow-lg border border-gray-200 dark:border-gray-700
                      z-50">
          <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-700">
            <p className="text-sm font-medium text-gray-900 dark:text-white">
              {user.name}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
              {user.email}
            </p>
          </div>
          <button
            onClick={() => {
              signOut()
              setIsOpen(false)
            }}
            className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-200 
                     hover:bg-gray-100 dark:hover:bg-gray-700 
                     flex items-center gap-2"
          >
            <LogOut className="w-4 h-4" />
            Sign out
          </button>
        </div>
      )}
    </div>
  )
} 
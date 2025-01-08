import { FC } from 'react'

export const UserMenu: FC = () => {
  return (
    <button 
      className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 
                 hover:bg-gray-100 dark:hover:bg-gray-800 
                 rounded-md transition-colors"
    >
      Sign in
    </button>
  )
} 
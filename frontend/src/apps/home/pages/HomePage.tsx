import { FC } from 'react'
import { useAuth } from '@/shared/contexts/AuthContext'
import { Navigate } from 'react-router-dom'

const HomePage: FC = () => {
  const { user, isLoading, isNewUser } = useAuth()

  console.log('HomePage render - isNewUser:', isNewUser)
  console.log('HomePage render - user:', user)

  if (isLoading) {
    return <div>Loading...</div>
  }

  if (!user) {
    return <Navigate to="/files" replace />
  }

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          {isNewUser 
            ? `Welcome onboard, ${user.name || 'User'}!`
            : `Welcome back, ${user.name || 'User'}!`
          }
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          {isNewUser
            ? "Your account has been created successfully. Let's get started!"
            : "We're glad to see you again."
          }
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Your Profile
        </h2>
        <div className="space-y-2">
          <div className="flex items-center space-x-2">
            <span className="text-gray-500 dark:text-gray-400">Email:</span>
            <span className="text-gray-900 dark:text-white">{user.email}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-gray-500 dark:text-gray-400">Last Login:</span>
            <span className="text-gray-900 dark:text-white">{user.lastLogin.toLocaleString()}</span>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button className="p-4 text-left rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <h3 className="font-medium text-gray-900 dark:text-white">Upload Files</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">Upload new files for processing</p>
          </button>
          <button className="p-4 text-left rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <h3 className="font-medium text-gray-900 dark:text-white">View Recent Files</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">Check your recently processed files</p>
          </button>
        </div>
      </div>
    </div>
  )
}

export { HomePage } 
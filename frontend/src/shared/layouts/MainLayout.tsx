import { FC, ReactNode } from 'react'
import { NavigationBar } from '../components/NavigationBar'

interface MainLayoutProps {
  children: ReactNode
}

const MainLayout: FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <NavigationBar />
      <main className="container mx-auto py-6 px-4">
        {children}
      </main>
    </div>
  )
}

export { MainLayout }
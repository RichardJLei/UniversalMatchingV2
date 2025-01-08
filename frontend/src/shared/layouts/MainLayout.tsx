import { FC, ReactNode } from 'react'
import { Header } from '../components/Header'
import { Footer } from '../components/Footer'

interface MainLayoutProps {
  children: ReactNode
}

const MainLayout: FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <Header />
      <main className="container mx-auto py-6 px-4 flex-1">
        {children}
      </main>
      <Footer />
    </div>
  )
}

export { MainLayout }
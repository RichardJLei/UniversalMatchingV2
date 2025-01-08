import { FC } from 'react'
import { Logo } from './Logo'
import { NavigationBar } from './NavigationBar'
import { UserMenu } from './UserMenu'
import { ThemeToggle } from './ThemeToggle'

export const Header: FC = () => {
  return (
    <header className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 transition-colors">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between gap-4">
          <div className="flex items-center gap-8">
            <Logo />
            <NavigationBar />
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <UserMenu />
          </div>
        </div>
      </div>
    </header>
  )
} 
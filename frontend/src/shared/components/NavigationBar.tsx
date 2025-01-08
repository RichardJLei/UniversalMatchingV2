import { FC } from 'react'
import { Link } from 'react-router-dom'

const NavigationBar: FC = () => {
  const navItems = [
    { label: 'File Management', href: '/files' },
    { label: 'Parse Files', href: '/parser' },
    { label: 'Compare Files', href: '/comparison' },
    { label: 'User Management', href: '/users' }
  ]

  return (
    <nav>
      <div className="flex items-center space-x-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            to={item.href}
            className="px-3 py-2 rounded-md text-sm font-medium 
                       text-gray-600 dark:text-gray-300 
                       hover:text-gray-900 dark:hover:text-white 
                       hover:bg-gray-100 dark:hover:bg-gray-800 
                       transition-colors"
          >
            {item.label}
          </Link>
        ))}
      </div>
    </nav>
  )
}

export { NavigationBar }
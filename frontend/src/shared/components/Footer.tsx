import { FC } from 'react'
import { Link } from 'react-router-dom'

const footerLinks = [
  { label: 'Privacy Policy', href: '/privacy' },
  { label: 'Terms of Service', href: '/terms' },
  { label: 'Contact Support', href: '/support' },
  { label: 'About Us', href: '/about' }
]

export const Footer: FC = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="mt-auto border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 transition-colors">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center space-y-4">
          <nav className="flex flex-wrap justify-center gap-x-8 gap-y-2">
            {footerLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className="text-sm text-gray-600 dark:text-gray-400 
                         hover:text-gray-900 dark:hover:text-white 
                         transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </nav>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            © {currentYear} PDF Processor. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  )
} 
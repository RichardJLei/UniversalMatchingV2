import { FC } from 'react'
import { FileText } from 'lucide-react'
import { Link } from 'react-router-dom'

export const Logo: FC = () => {
  return (
    <Link 
      to="/" 
      className="flex items-center gap-2 text-gray-900 dark:text-white hover:opacity-90"
    >
      <FileText className="h-6 w-6" />
      <span className="font-semibold text-lg">PDF Processor</span>
    </Link>
  )
} 
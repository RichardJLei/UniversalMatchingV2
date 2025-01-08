import { FC } from 'react'

const FileListPage: FC = () => {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
        Received Files
      </h1>
      <div className="rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
        <p className="text-gray-600 dark:text-gray-300">
          File list will be displayed here
        </p>
      </div>
    </div>
  )
}

export { FileListPage }
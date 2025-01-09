import { FC } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { MainLayout } from '../layouts/MainLayout'
import { HomePage } from '../../apps/home/pages/HomePage'
import { FileListPage } from '../../apps/files/pages/FileListPage'
import { ParserPage } from '../../apps/parser/pages/ParserPage'
import { ComparisonPage } from '../../apps/comparison/pages/ComparisonPage'
import { UserManagementPage } from '../../apps/users/pages/UserManagementPage'

const AppRouter: FC = () => {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/home" element={<HomePage />} />
          <Route path="/files" element={<FileListPage />} />
          <Route path="/parser" element={<ParserPage />} />
          <Route path="/comparison" element={<ComparisonPage />} />
          <Route path="/users" element={<UserManagementPage />} />
          <Route path="/" element={<Navigate to="/home" replace />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  )
}

export { AppRouter }
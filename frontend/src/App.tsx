import { FC } from 'react'
import { AppRouter } from '@/shared/components/AppRouter'
import { ThemeProvider } from '@/shared/contexts/ThemeContext'
import { AuthProvider } from '@/shared/contexts/AuthContext'

const App: FC = () => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AppRouter />
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App

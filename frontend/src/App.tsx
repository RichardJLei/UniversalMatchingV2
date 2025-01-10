import { FC } from 'react'
import { AppRouter } from '@/shared/components/AppRouter'
import { ThemeProvider } from '@/shared/contexts/ThemeContext'

const App: FC = () => {
  return (
    <ThemeProvider>
      <AppRouter />
    </ThemeProvider>
  )
}

export default App

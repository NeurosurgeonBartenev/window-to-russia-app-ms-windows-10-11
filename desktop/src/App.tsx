import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import './DesktopApp.css'

function DesktopApp() {
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAuthStore()
  const [wallpaper, setWallpaper] = React.useState<any>(null)
  const [isLoading, setIsLoading] = React.useState(true)

  // Listen for tray menu events
  useEffect(() => {
    if (window.electron) {
      window.electron.onChangeWallpaper(() => {
        setWallpaper(null)
        navigate('/today')
      })

      window.electron.onOpenSettings(() => {
        navigate('/settings')
      })
    }
  }, [navigate])

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setIsLoading(false), 1000)
  }, [])

  if (!isAuthenticated) {
    return (
      <div className="desktop-app">
        <div className="welcome-screen">
          <h1>🪟 Window to RUSSIA</h1>
          <p>Desktop Application</p>
          <button onClick={() => navigate('/login')}>Login</button>
        </div>
      </div>
    )
  }

  return (
    <div className="desktop-app">
      <div className="desktop-header">
        <h1>🪟 Window to RUSSIA</h1>
        <div className="user-info">
          <span>{user?.username}</span>
        </div>
      </div>

      <div className="desktop-content">
        {isLoading ? (
          <div className="loading">Loading...</div>
        ) : (
          <div className="wallpaper-grid">
            {/* Wallpapers will be displayed here */}
            <p>Click on an image to set it as wallpaper or lock screen</p>
          </div>
        )}
      </div>

      <div className="desktop-footer">
        <p>
          Right-click the tray icon for more options | 🔄 Auto-refresh every
          minute
        </p>
      </div>
    </div>
  )
}

export default DesktopApp

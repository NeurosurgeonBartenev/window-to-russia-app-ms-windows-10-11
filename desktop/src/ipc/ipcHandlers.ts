import { ipcMain } from 'electron'
import { wallpaperManager } from '../services/wallpaperManager'
import { settingsManager } from '../services/settingsManager'

export function registerIpcHandlers(): void {
  // Wallpaper handlers
  ipcMain.handle('set-wallpaper', async (event, wallpaperId: string, imageUrl: string) => {
    try {
      await wallpaperManager.setWallpaper(imageUrl)
      return { success: true }
    } catch (error) {
      return { success: false, error: (error as Error).message }
    }
  })

  ipcMain.handle('set-lock-screen', async (event, imageUrl: string) => {
    try {
      await wallpaperManager.setLockScreen(imageUrl)
      return { success: true }
    } catch (error) {
      return { success: false, error: (error as Error).message }
    }
  })

  // Settings handlers
  ipcMain.handle('get-settings', async () => {
    try {
      const settings = await settingsManager.getSettings()
      return settings
    } catch (error) {
      return { error: (error as Error).message }
    }
  })

  ipcMain.handle('save-settings', async (event, settings) => {
    try {
      await settingsManager.saveSettings(settings)
      return { success: true }
    } catch (error) {
      return { success: false, error: (error as Error).message }
    }
  })
}

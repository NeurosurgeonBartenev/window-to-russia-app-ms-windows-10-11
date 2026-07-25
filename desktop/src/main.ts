import { app, BrowserWindow, ipcMain, Menu, Tray } from 'electron'
import path from 'path'
import isDev from 'electron-is-dev'
import { createWindow } from './windows/mainWindow'
import { setupTrayMenu } from './tray/trayMenu'
import { registerIpcHandlers } from './ipc/ipcHandlers'

let mainWindow: BrowserWindow | null = null
let tray: Tray | null = null

app.on('ready', () => {
  mainWindow = createWindow()
  registerIpcHandlers()
  setupTrayMenu(app, mainWindow)
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    mainWindow = createWindow()
  }
})

// Handle app termination
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error)
})

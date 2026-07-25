import { app, Menu, Tray, BrowserWindow } from 'electron'
import path from 'path'

export function setupTrayMenu(
  app: typeof import('electron').app,
  mainWindow: BrowserWindow,
): void {
  const trayIconPath = path.join(__dirname, '../../assets/icon.png')

  const tray = new Tray(trayIconPath)

  const contextMenu = Menu.buildFromTemplate([
    {
      label: '🪟 Show Window',
      click: () => {
        if (mainWindow.isVisible()) {
          mainWindow.hide()
        } else {
          mainWindow.show()
        }
      },
    },
    {
      label: '🖼️ Change Wallpaper',
      click: () => {
        mainWindow.show()
        mainWindow.webContents.send('change-wallpaper')
      },
    },
    {
      label: '⚙️ Settings',
      click: () => {
        mainWindow.show()
        mainWindow.webContents.send('open-settings')
      },
    },
    { type: 'separator' },
    {
      label: '❌ Exit',
      click: () => {
        app.quit()
      },
    },
  ])

  tray.setContextMenu(contextMenu)

  tray.on('double-click', () => {
    if (mainWindow.isVisible()) {
      mainWindow.hide()
    } else {
      mainWindow.show()
    }
  })
}

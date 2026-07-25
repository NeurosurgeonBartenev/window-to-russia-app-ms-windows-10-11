import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electron', {
  setWallpaper: (wallpaperId: string, imageUrl: string) =>
    ipcRenderer.invoke('set-wallpaper', wallpaperId, imageUrl),

  setLockScreen: (imageUrl: string) =>
    ipcRenderer.invoke('set-lock-screen', imageUrl),

  getSettings: () => ipcRenderer.invoke('get-settings'),

  saveSettings: (settings: any) =>
    ipcRenderer.invoke('save-settings', settings),

  onChangeWallpaper: (callback: () => void) =>
    ipcRenderer.on('change-wallpaper', callback),

  onOpenSettings: (callback: () => void) =>
    ipcRenderer.on('open-settings', callback),
})

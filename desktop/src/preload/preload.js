const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('wallpaperAPI', {
  apply: (wallpaperId) => ipcRenderer.invoke('wallpaper:apply', wallpaperId),
  getToday: () => ipcRenderer.invoke('wallpaper:getToday'),
  getCurrentWallpaper: () => ipcRenderer.invoke('wallpaper:getCurrent'),
  openSettings: () => ipcRenderer.invoke('app:openSettings')
});

contextBridge.exposeInMainWorld('appAPI', {
  minimize: () => ipcRenderer.invoke('app:minimize'),
  maximize: () => ipcRenderer.invoke('app:maximize'),
  close: () => ipcRenderer.invoke('app:close'),
  getAppVersion: () => ipcRenderer.invoke('app:getVersion')
});

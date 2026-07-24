const { app, BrowserWindow, Menu, ipcMain, Tray } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const WallpaperManager = require('./src/main/wallpaper-manager');
const ScheduleManager = require('./src/main/schedule-manager');

let mainWindow;
let tray;
const wallpaperManager = new WallpaperManager();
const scheduleManager = new ScheduleManager(wallpaperManager);

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'src/preload/preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false
    }
  });

  const startUrl = isDev
    ? 'http://localhost:5173'
    : `file://${path.join(__dirname, '../frontend/build/index.html')}`;

  mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function createTray() {
  const iconPath = path.join(__dirname, '../assets/icon.png');
  tray = new Tray(iconPath);

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Open',
      click: () => {
        if (mainWindow) {
          mainWindow.show();
        } else {
          createWindow();
        }
      }
    },
    {
      label: 'Quit',
      click: () => {
        app.quit();
      }
    }
  ]);

  tray.setContextMenu(contextMenu);
}

app.on('ready', () => {
  createWindow();
  createTray();
  scheduleManager.start();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// IPC Handlers
ipcMain.handle('wallpaper:apply', async (event, wallpaperId) => {
  try {
    await wallpaperManager.applyWallpaper(wallpaperId);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('wallpaper:getToday', async () => {
  try {
    const wallpaper = await wallpaperManager.getTodayWallpaper();
    return { success: true, data: wallpaper };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

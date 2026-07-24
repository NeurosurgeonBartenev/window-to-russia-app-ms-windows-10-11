const { execSync } = require('child_process');
const path = require('path');
const axios = require('axios');

class WallpaperManager {
  constructor() {
    this.apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
  }

  async applyWallpaper(wallpaperId) {
    try {
      // Get wallpaper details
      const response = await axios.get(`${this.apiUrl}/wallpapers/${wallpaperId}`);
      const wallpaperUrl = response.data.image_4k_url || response.data.image_url;

      // Download image
      const imagePath = path.join(process.env.APPDATA, 'WindowToRussia', `wallpaper-${wallpaperId}.jpg`);
      await this.downloadImage(wallpaperUrl, imagePath);

      // Apply wallpaper using Windows API
      this.applyWallpaperWindows(imagePath);

      return { success: true, message: 'Wallpaper applied successfully' };
    } catch (error) {
      throw new Error(`Failed to apply wallpaper: ${error.message}`);
    }
  }

  async downloadImage(url, destination) {
    const response = await axios.get(url, { responseType: 'stream' });
    // Implementation for downloading file
  }

  applyWallpaperWindows(imagePath) {
    const vbsScript = `
Set objWallpaper = CreateObject("WScript.Shell")
objWallpaper.RegWrite "HKEY_CURRENT_USER\\Control Panel\\Desktop\\Wallpaper", "${imagePath}"
objWallpaper.Run "rundll32.exe user32.dll,UpdatePerUserSystemParameters 1, True"
    `;
    // Execute VBS script
  }

  async getTodayWallpaper() {
    try {
      const response = await axios.get(`${this.apiUrl}/wallpapers/today`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get today's wallpaper: ${error.message}`);
    }
  }
}

module.exports = WallpaperManager;

import { execSync } from 'child_process'
import path from 'path'
import os from 'os'
import fs from 'fs'

export class WallpaperManager {
  async setWallpaper(imageUrl: string): Promise<void> {
    const platform = process.platform

    if (platform === 'win32') {
      await this.setWallpaperWindows(imageUrl)
    } else if (platform === 'darwin') {
      await this.setWallpaperMac(imageUrl)
    } else if (platform === 'linux') {
      await this.setWallpaperLinux(imageUrl)
    }
  }

  private async setWallpaperWindows(imageUrl: string): Promise<void> {
    // Download image
    const imagePath = await this.downloadImage(imageUrl)

    // Use Windows API via PowerShell
    const psScript = `
      Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Wallpaper {
          [DllImport("user32.dll", CharSet = CharSet.Auto)]
          public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
          public static void SetWallpaper(string path) {
            SystemParametersInfo(20, 0, path, 3);
          }
        }
      "@
      [Wallpaper]::SetWallpaper("${imagePath}")
    `

    execSync(`powershell -Command "${psScript}"`)
  }

  private async setWallpaperMac(imageUrl: string): Promise<void> {
    const imagePath = await this.downloadImage(imageUrl)

    const script = `
      tell application "Finder"
        set desktop picture to POSIX file "${imagePath}"
      end tell
    `

    execSync(`osascript -e '${script}'`)
  }

  private async setWallpaperLinux(imageUrl: string): Promise<void> {
    const imagePath = await this.downloadImage(imageUrl)

    // Try different desktop environments
    try {
      // GNOME
      execSync(
        `gsettings set org.gnome.desktop.background picture-uri "file://${imagePath}"`,
      )
    } catch {
      try {
        // KDE
        execSync(
          `qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript 'var Desktops = desktops(); for (i=0;i<Desktops.length;i++) { d = Desktops[i]; d.wallpaperPlugin = "org.kde.image"; d.currentConfigGroup = Array("Wallpaper","org.kde.image","General"); d.writeConfig("Image", "file://${imagePath}") }'`,
        )
      } catch {
        // Fallback for other DEs
        console.log('Could not set wallpaper on this Linux desktop environment')
      }
    }
  }

  async setLockScreen(imageUrl: string): Promise<void> {
    const platform = process.platform

    if (platform === 'win32') {
      await this.setLockScreenWindows(imageUrl)
    } else if (platform === 'darwin') {
      console.log('Lock screen wallpaper not fully supported on macOS')
    } else if (platform === 'linux') {
      console.log('Lock screen wallpaper not fully supported on Linux')
    }
  }

  private async setLockScreenWindows(imageUrl: string): Promise<void> {
    const imagePath = await this.downloadImage(imageUrl)

    const lockScreenPath = path.join(
      process.env.APPDATA || '',
      'Microsoft',
      'Windows',
      'Themes',
    )

    const destPath = path.join(lockScreenPath, 'lockscreen.jpg')
    fs.copyFileSync(imagePath, destPath)

    const regPath = 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes'
    execSync(`reg add "${regPath}" /v LockScreenPath /d "${destPath}" /f`)
  }

  private async downloadImage(imageUrl: string): Promise<string> {
    const https = await import('https')
    const http = await import('http')
    const tmpDir = os.tmpdir()
    const fileName = `wallpaper-${Date.now()}.jpg`
    const filePath = path.join(tmpDir, fileName)

    return new Promise((resolve, reject) => {
      const protocol = imageUrl.startsWith('https') ? https : http
      const file = fs.createWriteStream(filePath)

      protocol.get(imageUrl, (response) => {
        response.pipe(file)
        file.on('finish', () => {
          file.close()
          resolve(filePath)
        })
      }).on('error', (error) => {
        fs.unlink(filePath, () => {})
        reject(error)
      })
    })
  }
}

export const wallpaperManager = new WallpaperManager()

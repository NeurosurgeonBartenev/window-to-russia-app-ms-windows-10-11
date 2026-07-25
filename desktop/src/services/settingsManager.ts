import path from 'path'
import os from 'os'
import fs from 'fs'

interface Settings {
  autoChangeWallpaper: boolean
  changeInterval: number // in minutes
  enableLockScreen: boolean
  autoStartOnBoot: boolean
  useLocalImages: boolean
  imagePath?: string
}

export class SettingsManager {
  private configDir: string
  private configFile: string
  private defaultSettings: Settings = {
    autoChangeWallpaper: false,
    changeInterval: 60,
    enableLockScreen: false,
    autoStartOnBoot: false,
    useLocalImages: false,
  }

  constructor() {
    this.configDir = path.join(os.homedir(), '.windowtorussia')
    this.configFile = path.join(this.configDir, 'settings.json')
    this.ensureConfigDir()
  }

  private ensureConfigDir(): void {
    if (!fs.existsSync(this.configDir)) {
      fs.mkdirSync(this.configDir, { recursive: true })
    }
  }

  async getSettings(): Promise<Settings> {
    try {
      if (fs.existsSync(this.configFile)) {
        const data = fs.readFileSync(this.configFile, 'utf-8')
        return JSON.parse(data)
      }
      return this.defaultSettings
    } catch (error) {
      console.error('Error reading settings:', error)
      return this.defaultSettings
    }
  }

  async saveSettings(settings: Partial<Settings>): Promise<void> {
    try {
      const currentSettings = await this.getSettings()
      const updatedSettings = { ...currentSettings, ...settings }
      fs.writeFileSync(this.configFile, JSON.stringify(updatedSettings, null, 2))
    } catch (error) {
      console.error('Error saving settings:', error)
      throw error
    }
  }
}

export const settingsManager = new SettingsManager()

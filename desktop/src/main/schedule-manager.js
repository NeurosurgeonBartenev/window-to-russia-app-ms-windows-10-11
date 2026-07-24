const cron = require('node-cron');

class ScheduleManager {
  constructor(wallpaperManager) {
    this.wallpaperManager = wallpaperManager;
    this.tasks = [];
  }

  start() {
    // Schedule daily wallpaper update at midnight
    const dailyTask = cron.schedule('0 0 * * *', async () => {
      console.log('Running daily wallpaper update...');
      try {
        const wallpaper = await this.wallpaperManager.getTodayWallpaper();
        await this.wallpaperManager.applyWallpaper(wallpaper.wallpapers[0].id);
        console.log('Daily wallpaper updated successfully');
      } catch (error) {
        console.error('Failed to update daily wallpaper:', error);
      }
    });

    this.tasks.push(dailyTask);
    console.log('Schedule manager started');
  }

  stop() {
    this.tasks.forEach(task => task.stop());
    console.log('Schedule manager stopped');
  }
}

module.exports = ScheduleManager;

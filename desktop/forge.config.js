const path = require('path')
const isDev = require('electron-is-dev')

module.exports = {
  packagerConfig: {
    asar: true,
    icon: path.join(__dirname, 'assets/icon'),
  },
  rebuildConfig: {},
  makers: [
    {
      name: '@electron-forge/maker-squirrel',
      config: {
        certificateFile: process.env.WINDOWS_CERTIFICATE_FILE,
        certificatePassword: process.env.WINDOWS_CERTIFICATE_PASSWORD,
        signWithParams: `/f ${process.env.WINDOWS_CERTIFICATE_FILE} /p ${process.env.WINDOWS_CERTIFICATE_PASSWORD}`,
      },
    },
    {
      name: '@electron-forge/maker-zip',
      platforms: ['darwin', 'linux'],
    },
    {
      name: '@electron-forge/maker-deb',
      config: {},
    },
  ],
  plugins: [
    {
      name: '@electron-forge/plugin-webpack',
      config: {
        mainConfig: './webpack.main.config.js',
        renderer: {
          config: './webpack.renderer.config.js',
          preload: {
            js: './src/preload.ts',
          },
        },
      },
    },
  ],
}

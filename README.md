# 🪟 Window to RUSSIA - Wallpaper Application

A modern desktop application that showcases the beauty, culture, and heritage of Russia through daily curated wallpapers and educational content.

## 📋 Project Overview

**Window to RUSSIA** is a sophisticated wallpaper management application designed to compete with Microsoft Bing's wallpaper service. The application delivers daily themed collections featuring Russian regions, cultural heritage sites, and landmarks with rich educational content.

### Key Features

#### Core Functionality
- 🎨 **Daily Wallpaper Collections** - New theme every day (Russian regions, cultural heritage sites, landmarks, etc.)
- 🔄 **Auto-Rotation** - Wallpapers change automatically on desktop and lock screen
- 📺 **Lock Screen Slideshow** - Full day's collection displays on lock screen
- 🌍 **Multi-Language Support** - 8 languages: RU, EN, ZH, DE, IT, FR, JA, ES
- 👤 **User Accounts** - Personal dashboard with favorites and wishlist
- 📱 **Cross-Platform** - Windows first, then macOS, Linux, iOS, Android

#### Personal Cabinet Features
- ⭐ **Favorites Management** - Save favorite wallpapers
- 🎯 **Places Wishlist** - Mark places to visit
- 📚 **Collection Archive** - Browse previous daily themes
- 💳 **Subscription Management** - View active subscriptions
- 🔐 **Multi-Social Login** - 15+ authentication providers

#### User Interface
- "Today's Theme" button - View current day's collection
- "About Project" button - Learn about the application
- Main dashboard with theme preview and invitation
- Modern, colorful, responsive design

## 🎯 Social Login Providers

- Google
- Yandex
- VK.com
- X.com (Twitter)
- Apple
- Microsoft
- WeChat
- QQ
- WhatsApp
- Telegram
- Snapchat
- Instagram
- LINE
- KakaoTalk
- Facebook

## 🌐 Supported Languages

1. Русский (Russian)
2. English
3. 中文 (Chinese)
4. Deutsch (German)
5. Italiano (Italian)
6. Français (French)
7. 日本語 (Japanese)
8. Español (Spanish)

## 🗂️ Project Structure

```
window-to-russia/
├── docs/
│   ├── architecture.md
│   ├── api-specification.md
│   ├── design-system.md
│   └── deployment.md
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── auth/
│   │   └── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── i18n/
│   │   ├── styles/
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
├── desktop/
│   ├── src/
│   │   ├── main/
│   │   ├── preload/
│   │   └── renderer/
│   ├── package.json
│   └── electron.js
├── config/
│   ├── social-providers.json
│   └── environments.json
├── .github/
│   └── workflows/
└── package.json
```

## 🚀 Development Phases

### Phase 1: Windows Desktop Application (Current Focus)
- [ ] Backend API development
- [ ] Windows desktop client (Electron)
- [ ] User authentication system
- [ ] Wallpaper management system
- [ ] Multilingual interface

### Phase 2: Feature Expansion
- [ ] Advanced analytics
- [ ] Social features
- [ ] Premium subscriptions
- [ ] Community contributions

### Phase 3: Cross-Platform
- [ ] macOS application
- [ ] Linux support
- [ ] iOS app
- [ ] Android app

## 💻 Tech Stack

### Backend
- **Runtime**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Storage**: S3-compatible
- **Authentication**: OAuth 2.0

### Frontend (Web Dashboard)
- **Framework**: React 18+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **i18n**: i18next

### Desktop (Windows)
- **Framework**: Electron
- **Language**: TypeScript
- **Wallpaper Management**: Windows API
- **Scheduled Tasks**: Node-cron

## 📊 Daily Theme Structure

Each daily theme includes:
- **Title & Description** - Historical/cultural background
- **10 Wallpaper Options** - High-resolution images (4K+)
- **Location Information** - GPS coordinates, descriptions, travel info
- **Educational Content** - Brief historical narrative
- **Category Tags** - Region, heritage type, era, etc.

## 🔐 Authentication Flow

```
User → Social Provider → Backend API → User Dashboard
       (Google, Yandex, etc.)
```

## 📱 User Features

### Main Dashboard
- Quick preview of today's theme
- Call-to-action to explore collection
- Quick links to accounts

### Today's Theme Section
- Gallery view (10 images)
- Image descriptions & locations
- "Like" button
- "Add to Favorites" button
- "Mark as Place to Visit" button
- Wallpaper selection option

### Personal Cabinet
- Profile information
- Favorite wallpapers collection
- Places to visit wishlist
- Collection archive
- Subscription details
- Settings & preferences

## 🎨 Design Requirements

- Modern, colorful UI
- Responsive design
- Smooth animations
- Dark/Light mode support
- Accessibility compliance (WCAG)
- Performance optimized

## 🔧 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Redis 7+

### Installation

```bash
# Clone repository
git clone https://github.com/drbartenev-bit/WINDOW-to-RUSSIA-APP-MS-WINDOWS-10-11.git
cd WINDOW-to-RUSSIA-APP-MS-WINDOWS-10-11

# Install dependencies
npm install

# Setup backend
cd backend
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install

# Setup desktop
cd ../desktop
npm install
```

### Development

```bash
# Start backend
cd backend
python main.py

# Start frontend (in another terminal)
cd frontend
npm run dev

# Start desktop app (in another terminal)
cd desktop
npm start
```

## 📝 Documentation

See the [docs](./docs) folder for detailed documentation:
- [Architecture](./docs/architecture.md)
- [API Specification](./docs/api-specification.md)
- [Design System](./docs/design-system.md)

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## 📄 License

MIT License - see [LICENSE](./LICENSE) file for details

---

**Status**: Project Planning Phase  
**Last Updated**: 2026-07-24  
**Target Platform**: Windows 10-11  
**First Release**: TBD
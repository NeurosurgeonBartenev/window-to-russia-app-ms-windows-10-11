# 🏗��� Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Windows Desktop App (Electron)            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Main Window                                         │   │
│  │  ├─ Dashboard (Today's Theme)                       │   │
│  │  ├─ Personal Cabinet (User Account)                 │   │
│  │  ├─ About Project                                  │   │
│  │  └─ Settings & Preferences                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Wallpaper Manager                                   │   │
│  │  ├─ Apply to Desktop                                │   │
│  │  ├─ Apply to Lock Screen                            │   │
│  │  ├─ Schedule Auto-rotation                          │   │
│  │  └─ Windows API Integration                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Authentication Service                              │   │
│  │  ├─ OAuth 2.0 Integration                           │   │
│  │  ├─ Social Login Handlers (15+ providers)           │   │
│  │  ├─ JWT Token Management                            │   │
│  │  └─ User Sessions                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Wallpaper Service                                   │   │
│  │  ├─ Daily Theme Management                          │   │
│  │  ├─ Image Delivery (CDN)                            │   │
│  │  ├─ Collection Archive                              │   │
│  │  └─ Search & Filter                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  User Service                                        │   │
│  │  ├─ Profile Management                              │   │
│  │  ├─ Favorites Management                            │   │
│  │  ├─ Places Wishlist                                 │   │
│  │  ├─ Subscription Management                         │   │
│  │  └─ Preferences                                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   PostgreSQL     │  │    Redis     │  │  S3 Storage  │  │
│  │   (Primary DB)   │  │    (Cache)   │  │   (Images)   │  │
│  └──────────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture - Frontend

```
App
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   ├── LanguageSwitcher (8 languages)
│   │   └── UserMenu
│   └── Navigation
│       ├── Dashboard
│       ├── Today's Theme
│       ├── About Project
│       └── Personal Cabinet
├── Pages
│   ├── HomePage
│   │   ├── ThemePreview
│   │   └── CallToAction
│   ├── TodayThemePage
│   │   ├── GalleryView
│   │   ├── ImageCard (x10)
│   │   ├── LocationDetails
│   │   └── ActionButtons
│   ├── PersonalCabinet
│   │   ├── UserProfile
│   │   ├── FavoritesList
│   │   ├── PlacesWishlist
│   │   ├── CollectionArchive
│   │   └── SubscriptionInfo
│   ├── AboutProject
│   └── AuthPages
│       └── SocialLoginButtons (15+)
└── Services
    ├── api.ts
    ├── auth.ts
    └── storage.ts
```

## Component Architecture - Desktop (Electron)

```
Electron App
├── Main Process
│   ├── app.ts
│   ├── window.manager.ts
│   ├── wallpaper.manager.ts
│   ├── scheduler.ts
│   └── tray.manager.ts
├── Preload Scripts
│   └── preload.ts
└── Renderer Process
    └── React App
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  username VARCHAR UNIQUE,
  display_name VARCHAR,
  avatar_url VARCHAR,
  language VARCHAR DEFAULT 'en',
  theme ENUM('light', 'dark') DEFAULT 'dark',
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Daily Themes Table
```sql
CREATE TABLE daily_themes (
  id UUID PRIMARY KEY,
  date DATE UNIQUE,
  title VARCHAR,
  description TEXT,
  category VARCHAR,
  region VARCHAR,
  wallpapers_count INT,
  created_at TIMESTAMP,
  published_at TIMESTAMP
);
```

### Wallpapers Table
```sql
CREATE TABLE wallpapers (
  id UUID PRIMARY KEY,
  theme_id UUID FOREIGN KEY,
  title VARCHAR,
  description TEXT,
  image_url VARCHAR,
  thumbnail_url VARCHAR,
  location_latitude DECIMAL,
  location_longitude DECIMAL,
  location_name VARCHAR,
  location_description TEXT,
  order_index INT,
  created_at TIMESTAMP
);
```

### User Favorites Table
```sql
CREATE TABLE user_favorites (
  id UUID PRIMARY KEY,
  user_id UUID FOREIGN KEY,
  wallpaper_id UUID FOREIGN KEY,
  created_at TIMESTAMP,
  UNIQUE(user_id, wallpaper_id)
);
```

### Places Wishlist Table
```sql
CREATE TABLE places_wishlist (
  id UUID PRIMARY KEY,
  user_id UUID FOREIGN KEY,
  location_name VARCHAR,
  location_latitude DECIMAL,
  location_longitude DECIMAL,
  visited BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP
);
```

## API Endpoints

### Authentication
- `GET /api/auth/login/{provider}` - Initiate social login
- `POST /api/auth/callback/{provider}` - OAuth callback
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh JWT token

### Wallpapers
- `GET /api/wallpapers/today` - Get today's theme
- `GET /api/wallpapers/archive` - Get archive
- `GET /api/wallpapers/{id}` - Get specific wallpaper

### Users
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update profile

### Favorites
- `GET /api/users/me/favorites` - Get favorites
- `POST /api/users/me/favorites` - Add to favorites
- `DELETE /api/users/me/favorites/{id}` - Remove from favorites

### Places
- `GET /api/users/me/places` - Get places
- `POST /api/users/me/places` - Add place
- `PUT /api/users/me/places/{id}` - Update place status

## Security

- **Authentication**: OAuth 2.0 with JWT tokens
- **HTTPS**: All communications encrypted
- **CORS**: Properly configured
- **Secrets**: Environment variables
- **Rate Limiting**: API rate limits per user
- **Data Privacy**: User data encryption at rest

## Performance Optimization

- **CDN**: Image delivery via CDN
- **Caching**: Redis for frequently accessed data
- **Database Indexing**: Optimized for common queries
- **Image Optimization**: Automatic resizing & compression
- **Lazy Loading**: Images loaded on demand
- **Code Splitting**: Components split by route

## Deployment

- **Backend**: Docker container
- **Database**: PostgreSQL
- **Cache**: Redis
- **Storage**: S3 for images
- **Frontend**: Static hosting
- **Desktop**: MSIX installer for Windows
- **CI/CD**: GitHub Actions
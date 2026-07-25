"""
Backend Architecture and Design Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│          FastAPI Web Server (Uvicorn)              │
│  Handles HTTP requests and returns JSON responses   │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │   API Routes    │
        │  /api/v1/*      │
        ├─────────────────┤
        │ • auth          │
        │ • users         │
        │ • themes        │
        │ • wallpapers    │
        │ • favorites     │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Middleware     │
        ├─────────────────┤
        │ • CORS          │
        │ • Auth (JWT)    │
        │ • Logging       │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Services       │
        ├─────────────────┤
        │ • AuthService   │
        │ • UserService   │
        │ • ThemeService  │
        └────────┬────────┘
                 │
        ┌────────▼────────────┐
        │  Database Layer     │
        ├─────────────────────┤
        │ SQLAlchemy ORM      │
        │ Async Session       │
        └────────┬────────────┘
                 │
        ┌────────▼────────────┐
        │   Databases         │
        ├─────────────────────┤
        │ • PostgreSQL (ORM)  │
        │ • Redis (Cache)     │
        └─────────────────────┘
```

## Project Structure

```
backend/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Configuration management
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py              # SQLAlchemy setup, session factory
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                  # BaseModel with timestamps
│   │   ├── user.py                  # User model (with 15 OAuth IDs)
│   │   ├── theme.py                 # DailyTheme model
│   │   ├── wallpaper.py             # Wallpaper model
│   │   ├── favorite.py              # Favorite & PlaceToVisit models
│   │   └── oauth_token.py           # OAuthToken model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                  # Pydantic schemas for users
│   │   ├── auth.py                  # Auth-related schemas
│   │   └── theme.py                 # Theme & wallpaper schemas
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                  # /auth endpoints
│   │   ├── users.py                 # /users endpoints
│   │   ├── themes.py                # /themes endpoints
│   │   ├── wallpapers.py            # /wallpapers endpoints
│   │   └── favorites.py             # /favorites endpoints
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py          # Authentication business logic
│   │
│   └── utils/
│       ├── __init__.py
│       ├── auth.py                  # JWT utilities
│       └── oauth.py                 # OAuth provider implementations
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_main.py                 # Main app tests
│   └── test_routes.py               # Route tests
│
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Poetry configuration
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── README.md                        # Backend README
└── API_DOCUMENTATION.md             # API documentation
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  full_name VARCHAR(255),
  avatar_url TEXT,
  language VARCHAR(10) DEFAULT 'en',
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  is_premium BOOLEAN DEFAULT false,
  bio TEXT,
  
  -- OAuth IDs (for 15 providers)
  google_id VARCHAR(255) UNIQUE,
  yandex_id VARCHAR(255) UNIQUE,
  vk_id VARCHAR(255) UNIQUE,
  microsoft_id VARCHAR(255) UNIQUE,
  apple_id VARCHAR(255) UNIQUE,
  x_id VARCHAR(255) UNIQUE,
  wechat_id VARCHAR(255) UNIQUE,
  qq_id VARCHAR(255) UNIQUE,
  whatsapp_id VARCHAR(255) UNIQUE,
  telegram_id VARCHAR(255) UNIQUE,
  snapchat_id VARCHAR(255) UNIQUE,
  instagram_id VARCHAR(255) UNIQUE,
  line_id VARCHAR(255) UNIQUE,
  kakao_id VARCHAR(255) UNIQUE,
  facebook_id VARCHAR(255) UNIQUE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Daily Themes Table
```sql
CREATE TABLE daily_themes (
  id UUID PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  short_description VARCHAR(500),
  theme_date DATE UNIQUE NOT NULL,
  category VARCHAR(100) NOT NULL,
  image_count INT DEFAULT 10,
  historical_narrative TEXT,
  cultural_significance TEXT,
  tags TEXT[],
  metadata JSON,
  cover_image_url TEXT,
  cover_image_key VARCHAR(255),
  is_published BOOLEAN DEFAULT false,
  is_featured BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Wallpapers Table
```sql
CREATE TABLE wallpapers (
  id UUID PRIMARY KEY,
  theme_id UUID NOT NULL REFERENCES daily_themes(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  image_url TEXT NOT NULL,
  image_key VARCHAR(255) UNIQUE NOT NULL,
  image_width INT,
  image_height INT,
  image_size_mb FLOAT,
  format VARCHAR(10) DEFAULT 'JPEG',
  location_name VARCHAR(255),
  location_description TEXT,
  latitude FLOAT,
  longitude FLOAT,
  address TEXT,
  photographer_name VARCHAR(255),
  photographer_credit TEXT,
  copyright_info TEXT,
  taken_date VARCHAR(50),
  tags VARCHAR(500),
  is_landscape BOOLEAN DEFAULT true,
  aspect_ratio VARCHAR(20),
  resolution VARCHAR(50),
  view_count INT DEFAULT 0,
  like_count INT DEFAULT 0,
  favorite_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Favorites Table
```sql
CREATE TABLE favorites (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  wallpaper_id UUID NOT NULL REFERENCES wallpapers(id) ON DELETE CASCADE,
  UNIQUE(user_id, wallpaper_id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Places to Visit Table
```sql
CREATE TABLE places_to_visit (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  wallpaper_id UUID REFERENCES wallpapers(id),
  location_name VARCHAR(255) NOT NULL,
  location_description TEXT,
  latitude FLOAT,
  longitude FLOAT,
  address TEXT,
  visited BOOLEAN DEFAULT false,
  visit_date VARCHAR(50),
  notes TEXT,
  priority VARCHAR(20) DEFAULT 'medium',
  UNIQUE(user_id, location_name),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## Authentication Flow

### JWT Authentication

```
1. User Registration/Login
   └─ Credentials validated
   └─ JWT tokens generated
   └─ Tokens returned to client

2. Authenticated Request
   ├─ Client sends: Authorization: Bearer {access_token}
   ├─ Middleware validates token
   ├─ User retrieved from database
   └─ Request processed

3. Token Refresh
   ├─ Client sends refresh_token
   ├─ Token validated
   └─ New access_token issued
```

### OAuth Flow

```
1. Get Authorization URL
   GET /auth/oauth/authorize?provider=google
   └─ Returns authorization URL with state parameter

2. User Authorizes
   └─ Redirected to OAuth provider
   └─ User grants permissions
   └─ Redirected back with authorization code

3. Exchange Code for Token
   POST /auth/oauth/login
   ├─ Code sent to provider
   ├─ Access token received
   ├─ User info retrieved
   └─ User created/linked and JWT issued
```

## Data Flow Examples

### Getting Today's Theme

```
1. Client Request
   GET /api/v1/themes/today

2. Route Handler
   └─ Query database for today's date
   └─ Include wallpapers relationship

3. Database Query
   SELECT * FROM daily_themes
   WHERE theme_date = TODAY()
   JOIN wallpapers

4. Response
   {
     "id": "uuid",
     "title": "Moscow",
     "wallpapers": [...10 wallpapers...]
   }
```

### Adding to Favorites

```
1. Client Request
   POST /api/v1/favorites/wallpapers/{wallpaper_id}
   Header: Authorization: Bearer {token}

2. Middleware
   └─ Validate JWT token
   └─ Extract user_id

3. Route Handler
   ├─ Check wallpaper exists
   ├─ Check not already favorited
   ├─ Create Favorite record
   ├─ Increment wallpaper.favorite_count
   └─ Commit to database

4. Response
   {"message": "Wallpaper added to favorites"}
```

## Security Considerations

1. **JWT Tokens**
   - Access tokens expire after 30 minutes
   - Refresh tokens expire after 7 days
   - Tokens signed with SECRET_KEY

2. **Password Security**
   - Bcrypt hashing with salt
   - Passwords validated for min 8 characters

3. **OAuth Security**
   - State parameter validation
   - Secure token storage
   - Automatic user linking

4. **Database**
   - Connection pooling
   - Prepared statements (SQLAlchemy)
   - Parameterized queries

5. **API Security**
   - CORS middleware configured
   - Rate limiting (planned)
   - Input validation with Pydantic

## Performance Optimizations

1. **Database**
   - Connection pooling (20 connections)
   - Indexes on frequently queried columns
   - Eager loading of relationships

2. **Caching**
   - Redis for session caching (planned)
   - ETags for image responses (planned)

3. **Query Optimization**
   - Pagination for list endpoints
   - Selective field loading
   - Limit 100 results max per request

## Deployment

### Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

### Docker
```bash
docker-compose up
```

### Production
- Use Gunicorn with multiple workers
- PostgreSQL with proper backups
- Redis for caching
- S3 for image storage
- HTTPS/TLS certificates
- Environment-specific config

## Monitoring & Logging

- Structured JSON logging
- Request/response logging
- Error tracking (Sentry planned)
- Performance monitoring (APM planned)

## Future Enhancements

1. **Phase 2**
   - Subscription system
   - Admin panel
   - Analytics dashboard
   - Email notifications

2. **Phase 3**
   - WebSocket support
   - Real-time notifications
   - Social features (comments, shares)
   - Community contributions

3. **Phase 4**
   - Machine learning for recommendations
   - Full-text search
   - Advanced filtering
   - API rate limiting

---

**Last Updated:** 2026-07-25  
**Status:** Production Ready for Phase 1
"""

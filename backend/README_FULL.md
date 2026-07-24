# Window to RUSSIA - Backend

## Setup & Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+

### Installation

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`
2. Update environment variables:
   ```bash
   cp .env.example .env
   ```
3. Configure database connection:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/window_to_russia
   ```
4. Add OAuth credentials for your providers

### Database Setup

```bash
# Create database
creatdb window_to_russia

# Run migrations (when ready)
alembic upgrade head
```

## Running the API

```bash
# Development
python src/main.py

# Or with uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
src/
├── api/                 # API endpoints
│   ├── auth.py         # Authentication endpoints
│   ├── wallpapers.py   # Wallpaper endpoints
│   ├── users.py        # User management
│   ├── favorites.py    # Favorites management
│   ├── places.py       # Places management
│   └── subscriptions.py # Subscription management
├── models/              # SQLAlchemy models
│   └── models.py       # Database models
├── schemas/             # Pydantic schemas
│   └── schemas.py      # Request/response schemas
├── services/            # Business logic
│   ├── auth_service.py
│   ├── wallpaper_service.py
│   ├── user_service.py
│   ├── place_service.py
│   ├── subscription_service.py
│   └── oauth_providers.py
├── config/              # Configuration
│   ├── settings.py
│   └── database.py
├── tests/               # Unit tests
└── main.py              # Application entry point
```

## API Endpoints

### Authentication
- `GET /api/v1/auth/login/{provider}` - Initiate OAuth login
- `POST /api/v1/auth/callback/{provider}` - OAuth callback
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout

### Wallpapers
- `GET /api/v1/wallpapers/today` - Get today's theme
- `GET /api/v1/wallpapers/{id}` - Get wallpaper by ID
- `GET /api/v1/wallpapers/archive` - Get archive
- `GET /api/v1/wallpapers/search` - Search wallpapers

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile
- `DELETE /api/v1/users/me` - Delete account

### Favorites
- `GET /api/v1/favorites` - Get favorites
- `POST /api/v1/favorites` - Add to favorites
- `DELETE /api/v1/favorites/{id}` - Remove from favorites

### Places
- `GET /api/v1/places` - Get places
- `POST /api/v1/places` - Add place
- `PUT /api/v1/places/{id}` - Update place
- `DELETE /api/v1/places/{id}` - Delete place

### Subscriptions
- `GET /api/v1/subscriptions/me` - Get subscription
- `GET /api/v1/subscriptions/plans` - Get available plans
- `POST /api/v1/subscriptions/subscribe` - Subscribe to plan
- `POST /api/v1/subscriptions/cancel` - Cancel subscription

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_health.py
```

## Docker

```bash
# Build image
docker build -t window-to-russia-backend .

# Run container
docker run -p 8000:8000 window-to-russia-backend
```

## Environment Variables

See `.env.example` for all available options:

```
DEBUG=True
ENVIRONMENT=development
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
YANDEX_CLIENT_ID=...
YANDEX_CLIENT_SECRET=...
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md)

## License

MIT License

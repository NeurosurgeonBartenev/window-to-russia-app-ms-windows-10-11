"""
Setup and installation guide for the backend
"""

# Backend Setup & Installation Guide

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 14 or higher
- Redis 7 or higher
- pip or Poetry

## Quick Start with Docker

The easiest way to get started is using Docker Compose:

```bash
# Navigate to project root
cd window-to-russia-app-ms-windows-10-11

# Start all services
docker-compose up

# Backend will be available at http://localhost:8000
# API Documentation at http://localhost:8000/api/docs
```

## Manual Installation

### 1. Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

**Windows:**
Download from https://www.postgresql.org/download/windows/

### 2. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE USER window_user WITH PASSWORD 'window_password';
CREATE DATABASE window_to_russia OWNER window_user;
ALTER ROLE window_user SET client_encoding TO 'utf8';
ALTER ROLE window_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE window_user SET default_transaction_deferrable TO on;
ALTER ROLE window_user SET default_transaction_read_only TO off;
```

### 3. Install Redis

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo service redis-server start
```

**Windows:**
Download from https://github.com/microsoftarchive/redis/releases

### 4. Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your favorite editor
```

### 5. Configure Environment Variables

Edit `.env` file with your settings:

```env
# Database
DATABASE_URL=postgresql://window_user:window_password@localhost:5432/window_to_russia

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-super-secret-key-change-in-production

# OAuth Providers (get these from provider dashboards)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
# ... other OAuth credentials
```

### 6. Run Backend

```bash
# Start the backend server
python main.py

# Server will start at http://localhost:8000
```

### 7. Access API Documentation

- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc
- **Health Check:** http://localhost:8000/health

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_auth.py

# Run in watch mode
pytest-watch
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Lint with Flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/

# Sort imports with isort
isort src/ tests/

# Run all checks
black src/ tests/ && flake8 src/ tests/ && mypy src/ && isort src/ tests/
```

### Database Migrations (with Alembic)

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Environment Variables Reference

See `.env.example` for all available environment variables:

### Essential Variables
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT signing key
- `DEBUG` - Debug mode (True/False)
- `ENVIRONMENT` - Environment name (development/staging/production)

### OAuth Providers
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- `YANDEX_CLIENT_ID`, `YANDEX_CLIENT_SECRET`
- `VK_CLIENT_ID`, `VK_CLIENT_SECRET`
- And 12 more providers...

### AWS S3 (for image storage)
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_BUCKET_NAME`

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or specify different port
python main.py --port 8001
```

### Database Connection Error

```bash
# Check PostgreSQL is running
psql -U window_user -d window_to_russia -c "SELECT 1"

# Check DATABASE_URL in .env
echo $DATABASE_URL
```

### Import Errors

```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Permission Errors on Linux/macOS

```bash
# Give execution permission to main.py
chmod +x main.py
```

## Next Steps

1. **Configure OAuth Providers**
   - Get credentials from Google, Yandex, VK, etc.
   - Update `.env` file

2. **Setup S3 Bucket** (for production)
   - Create AWS S3 bucket
   - Add credentials to `.env`

3. **Create Admin User** (future)
   - Admin panel for managing themes
   - Creating daily theme collections

4. **Load Sample Data**
   - Create test themes and wallpapers
   - Add locations with images

## Production Deployment

See `DEPLOYMENT.md` for production setup instructions.

## Support

For issues or questions:
1. Check the logs
2. Review `API_DOCUMENTATION.md`
3. Check `ARCHITECTURE.md`
4. Open an issue on GitHub

---

**Last Updated:** 2026-07-25
"""

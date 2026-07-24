# 📡 API Specification

## Base URL
```
https://api.windowtorussia.com/api/v1
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

---

## Authentication Endpoints

### 1. Initiate Social Login
```http
GET /auth/login/{provider}
```

**Providers**: google, yandex, vk, twitter, apple, microsoft, wechat, qq, whatsapp, telegram, snapchat, instagram, line, kakao, facebook

**Query Parameters**:
- `redirect_uri` (required) - Where to redirect after login
- `state` (optional) - CSRF protection

**Response**:
```json
{
  "auth_url": "https://provider.com/oauth/authorize?...",
  "state": "random_state_string"
}
```

### 2. OAuth Callback
```http
POST /auth/callback/{provider}
```

**Request Body**:
```json
{
  "code": "authorization_code",
  "state": "state_from_login"
}
```

**Response** (200):
```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "display_name": "John Doe",
    "avatar_url": "https://...",
    "provider": "google"
  }
}
```

### 3. Refresh Token
```http
POST /auth/refresh
```

**Request Body**:
```json
{
  "refresh_token": "refresh_token"
}
```

**Response** (200):
```json
{
  "access_token": "new_jwt_token",
  "expires_in": 3600
}
```

### 4. Logout
```http
POST /auth/logout
Authorization: Bearer {jwt_token}
```

**Response** (200):
```json
{
  "message": "Successfully logged out"
}
```

---

## Wallpaper Endpoints

### 1. Get Today's Theme
```http
GET /wallpapers/today
```

**Query Parameters**:
- `language` (optional) - Language code (default: en)

**Response** (200):
```json
{
  "theme": {
    "id": "uuid",
    "date": "2026-07-24",
    "title": "Moscow - The Heart of Russia",
    "description": "Explore the capital city...",
    "category": "Cities",
    "region": "Central Russia",
    "wallpapers_count": 10
  },
  "wallpapers": [
    {
      "id": "uuid",
      "title": "Red Square",
      "image_url": "https://cdn.../wallpaper_1.jpg",
      "thumbnail_url": "https://cdn.../thumb_1.jpg",
      "location": {
        "name": "Red Square, Moscow",
        "latitude": 55.7558,
        "longitude": 37.6173
      }
    }
  ]
}
```

### 2. Get Archive
```http
GET /wallpapers/archive?page=1&per_page=20
```

**Response** (200):
```json
{
  "total": 730,
  "page": 1,
  "per_page": 20,
  "themes": [...]
}
```

---

## User Endpoints

### 1. Get Current User
```http
GET /users/me
Authorization: Bearer {jwt_token}
```

**Response** (200):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "display_name": "John Doe",
  "language": "en",
  "theme": "dark"
}
```

### 2. Update Profile
```http
PUT /users/me
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "display_name": "John Doe",
  "language": "ru",
  "theme": "dark"
}
```

---

## Favorites Endpoints

### 1. Get Favorites
```http
GET /users/me/favorites
Authorization: Bearer {jwt_token}
```

### 2. Add to Favorites
```http
POST /users/me/favorites
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "wallpaper_id": "uuid"
}
```

---

## Places Endpoints

### 1. Get Places
```http
GET /users/me/places
Authorization: Bearer {jwt_token}
```

### 2. Add Place
```http
POST /users/me/places
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "name": "Red Square",
  "latitude": 55.7558,
  "longitude": 37.6173
}
```

---

## Error Responses

### 400 - Bad Request
```json
{
  "error": "INVALID_REQUEST",
  "message": "Missing required parameter",
  "status": 400
}
```

### 401 - Unauthorized
```json
{
  "error": "UNAUTHORIZED",
  "message": "Invalid or expired token",
  "status": 401
}
```

### 404 - Not Found
```json
{
  "error": "NOT_FOUND",
  "message": "Resource not found",
  "status": 404
}
```

### 429 - Rate Limited
```json
{
  "error": "RATE_LIMITED",
  "message": "Too many requests",
  "status": 429
}
```

---

## Rate Limiting

- **Free Users**: 100 requests per hour
- **Premium Users**: 1000 requests per hour

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1690209600
```

---

## Pagination

All list endpoints support pagination:

```
GET /wallpapers/archive?page=1&per_page=20
```

Response format:
```json
{
  "total": 250,
  "page": 1,
  "per_page": 20,
  "total_pages": 13,
  "has_next": true,
  "has_previous": false,
  "data": [...]
}
```
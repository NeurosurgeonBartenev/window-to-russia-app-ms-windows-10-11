"""
Window to RUSSIA Backend API Documentation

## Overview

This is the backend API for the "Window to RUSSIA" wallpaper application. It provides endpoints for:
- User authentication and OAuth integration (15 providers)
- Daily theme management
- Wallpaper retrieval and statistics
- User favorites and wishlists
- Personal cabinet functionality

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## Supported OAuth Providers

1. Google
2. Yandex
3. VK.com
4. Microsoft
5. Apple
6. X (Twitter)
7. WeChat
8. QQ
9. WhatsApp
10. Telegram
11. Snapchat
12. Instagram
13. LINE
14. KakaoTalk
15. Facebook

## API Endpoints

### Authentication (`/auth`)

#### Register
- **POST** `/auth/register`
- Register a new user with email and password
- **Request:**
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }
  ```
- **Response:** User data + tokens

#### Login
- **POST** `/auth/login`
- Authenticate with email and password
- **Request:**
  ```json
  {
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response:** Access and refresh tokens

#### OAuth Login
- **POST** `/auth/oauth/authorize`
- Get OAuth authorization URL
- **Query Parameters:**
  - `provider`: OAuth provider name (google, yandex, vk, etc.)
  - `state`: Optional state parameter

- **POST** `/auth/oauth/login`
- Complete OAuth authentication
- **Request:**
  ```json
  {
    "provider": "google",
    "code": "authorization_code_from_provider"
  }
  ```

#### Refresh Token
- **POST** `/auth/refresh`
- Get new access token using refresh token
- **Request:**
  ```json
  {
    "refresh_token": "your_refresh_token"
  }
  ```

### Users (`/users`)

#### Get Current User
- **GET** `/users/me`
- Get authenticated user's profile
- **Auth Required:** Yes

#### Get User by ID
- **GET** `/users/{user_id}`
- Get public user information
- **Auth Required:** No

#### Update Profile
- **PUT** `/users/me`
- Update current user's profile
- **Auth Required:** Yes
- **Request:**
  ```json
  {
    "full_name": "John Doe",
    "avatar_url": "https://example.com/avatar.jpg",
    "language": "en",
    "bio": "Russia enthusiast"
  }
  ```

#### Delete Account
- **DELETE** `/users/me`
- Delete user account
- **Auth Required:** Yes

### Themes (`/themes`)

#### Get Today's Theme
- **GET** `/themes/today`
- Get today's daily theme with all wallpapers
- **Auth Required:** No
- **Response:** Theme with 10+ wallpapers

#### Get Theme by ID
- **GET** `/themes/{theme_id}`
- Get specific theme with all wallpapers
- **Auth Required:** No

#### List All Themes
- **GET** `/themes`
- List all published themes (paginated)
- **Query Parameters:**
  - `skip`: Offset (default: 0)
  - `limit`: Number of results (default: 30, max: 100)
  - `category`: Filter by category (region, heritage, landmark, etc.)
  - `featured_only`: Show only featured themes (default: false)
- **Auth Required:** No

#### Search Themes by Date
- **GET** `/themes/search/by-date`
- Search themes by date range
- **Query Parameters:**
  - `date_from`: Start date (YYYY-MM-DD)
  - `date_to`: End date (YYYY-MM-DD, optional)

#### Create Theme
- **POST** `/themes`
- Create new daily theme (admin only)
- **Auth Required:** Yes (admin)
- **Request:**
  ```json
  {
    "title": "Moscow - Capital of Russia",
    "description": "Explore Moscow's landmarks...",
    "theme_date": "2024-01-15",
    "category": "region",
    "historical_narrative": "Moscow was founded in...",
    "cultural_significance": "Moscow is the political and cultural center...",
    "tags": ["Moscow", "Architecture", "Historical"]
  }
  ```

### Wallpapers (`/wallpapers`)

#### Get Theme Wallpapers
- **GET** `/wallpapers/theme/{theme_id}`
- Get all wallpapers for a specific theme
- **Auth Required:** No
- **Response:** Array of 10 wallpapers with high-resolution URLs

#### Get Specific Wallpaper
- **GET** `/wallpapers/{wallpaper_id}`
- Get wallpaper details
- **Auth Required:** No
- **Note:** View count is incremented

#### Like Wallpaper
- **POST** `/wallpapers/{wallpaper_id}/like`
- Like a wallpaper
- **Auth Required:** No
- **Response:** Updated like count

#### Search Wallpapers by Location
- **POST** `/wallpapers/search/by-location`
- Search wallpapers by location name
- **Query Parameters:**
  - `location_name`: Location to search for

### Favorites (`/favorites`)

#### Get Favorite Wallpapers
- **GET** `/favorites/wallpapers`
- Get user's favorite wallpapers
- **Auth Required:** Yes

#### Add to Favorites
- **POST** `/favorites/wallpapers/{wallpaper_id}`
- Add wallpaper to favorites
- **Auth Required:** Yes

#### Remove from Favorites
- **DELETE** `/favorites/wallpapers/{wallpaper_id}`
- Remove wallpaper from favorites
- **Auth Required:** Yes

#### Get Places to Visit
- **GET** `/favorites/places`
- Get user's places wishlist
- **Auth Required:** Yes
- **Query Parameters:**
  - `visited`: Filter by visit status (true/false, optional)

#### Add Place to Wishlist
- **POST** `/favorites/places`
- Add place to wishlist
- **Auth Required:** Yes
- **Request:**
  ```json
  {
    "location_name": "Red Square",
    "location_description": "Historic square in Moscow",
    "latitude": 55.7539,
    "longitude": 37.6208,
    "address": "Red Square, Moscow, Russia",
    "priority": "high",
    "notes": "Must visit!"
  }
  ```

#### Update Place
- **PUT** `/favorites/places/{place_id}`
- Update place in wishlist
- **Auth Required:** Yes

#### Mark Place as Visited
- **POST** `/favorites/places/{place_id}/mark-visited`
- Mark place as visited
- **Auth Required:** Yes
- **Query Parameters:**
  - `visit_date`: Date of visit (optional)

#### Remove Place from Wishlist
- **DELETE** `/favorites/places/{place_id}`
- Remove place from wishlist
- **Auth Required:** Yes

## Response Format

All successful responses return JSON with the requested data.

### Error Response

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists
- `500 Internal Server Error` - Server error

## Rate Limiting

Currently no rate limiting is implemented. This will be added in production.

## WebSocket Support

Planned for future versions:
- Real-time notifications
- Live statistics updates
- Chat functionality

## Examples

### Complete Authentication Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "full_name": "John Doe"
  }'

# Response includes access_token and refresh_token

# 2. Get today's theme
curl http://localhost:8000/api/v1/themes/today

# 3. Add wallpaper to favorites
curl -X POST http://localhost:8000/api/v1/favorites/wallpapers/{wallpaper_id} \
  -H "Authorization: Bearer {access_token}"

# 4. Add place to wishlist
curl -X POST http://localhost:8000/api/v1/favorites/places \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "location_name": "Red Square",
    "latitude": 55.7539,
    "longitude": 37.6208,
    "priority": "high"
  }'
```

## Changelog

### v0.1.0 (2026-07-25)
- Initial API scaffold
- Authentication system (JWT + OAuth)
- User management
- Daily themes system
- Wallpaper management
- Favorites and wishlist

## Support

For issues or questions, please open an issue on GitHub.

---

**Last Updated:** 2026-07-25  
**Status:** Development
"""

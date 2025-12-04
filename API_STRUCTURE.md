# API Structure

This document describes the RESTful API structure with separate modules for each resource.

## Module Structure

```
app/
└── api/
    ├── __init__.py
    ├── auth/
    │   ├── __init__.py
    │   └── routes.py          # Authentication endpoints
    ├── users/
    │   ├── __init__.py
    │   └── routes.py          # User management endpoints
    └── organizations/
        ├── __init__.py
        └── routes.py          # Organization management endpoints
```

## API Endpoints

### Authentication API (`/api/auth`)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/api/auth/login` | Authenticate user and get JWT token | 200, 401, 404 |
| POST | `/api/auth/logout` | Logout current user | 200, 401 |
| GET | `/api/auth/status` | Get current user status | 200, 401, 404 |

### Users API (`/api/users`)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/api/users` | List all users | 200 |
| POST | `/api/users` | Create new user | 201, 400, 500 |
| GET | `/api/users/{id}` | Get user by ID | 200, 404 |
| PUT | `/api/users/{id}` | Update user by ID | 200, 404, 400 |
| DELETE | `/api/users/{id}` | Delete user by ID | 204, 404 |

### Organizations API (`/api/organizations`)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/api/organizations` | List all organizations | 200 |
| POST | `/api/organizations` | Create new organization | 201, 400, 500 |
| GET | `/api/organizations/{id}` | Get organization by ID | 200, 404 |
| PUT | `/api/organizations/{id}` | Update organization by ID | 200, 404, 400 |
| DELETE | `/api/organizations/{id}` | Delete organization by ID | 204, 404 |

## REST Standards Followed

### 1. Resource-Based URLs
- URLs represent resources (nouns, not verbs)
- Example: `/api/users` not `/api/getUsers`

### 2. HTTP Methods
- **GET**: Retrieve resources
- **POST**: Create new resources
- **PUT**: Update entire resource
- **DELETE**: Delete resource

### 3. HTTP Status Codes
- **200 OK**: Successful GET, PUT
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation errors
- **401 Unauthorized**: Authentication required
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server errors

### 4. Response Format
All responses follow consistent JSON structure:
```json
{
    "status": "success|error|fail",
    "message": "Human-readable message",
    "data": {
        // Response data
    }
}
```

## Benefits

1. **Separation of Concerns**: Each resource has its own module
2. **Maintainability**: Easy to find and modify specific endpoints
3. **Scalability**: Easy to add new endpoints to existing modules
4. **REST Compliance**: Follows REST architectural principles
5. **Clean Structure**: Clear organization without versioning complexity

## Module Responsibilities

### `app/api/auth/`
- User authentication
- JWT token generation
- User status retrieval

### `app/api/users/`
- User CRUD operations
- User listing
- Profile management

### `app/api/organizations/`
- Organization CRUD operations
- Organization listing
- Organization management

## Registration

All blueprints are registered in `app/__init__.py`:

```python
from app.api.auth import auth_bp
from app.api.users import users_bp
from app.api.organizations import organizations_bp

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(organizations_bp, url_prefix='/api')
```


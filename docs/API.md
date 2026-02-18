# API Documentation

This document provides comprehensive documentation for the API, including all endpoints, parameters, and examples.

## Base URL

The base URL for all API endpoints is: `https://api.yourservice.com/v1`

## Authentication

All requests must include an `Authorization` header with a valid API key:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Get All Items
- **Endpoint**: `/items`
- **Method**: `GET`
- **Query Parameters**:
  - `page` (optional): The page number to retrieve.
  - `limit` (optional): The number of items per page.

- **Example Request**:
```
GET /items?page=1&limit=10
Authorization: Bearer YOUR_API_KEY
```

- **Successful Response**:
```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "totalItems": 100
  }
}
```

### 2. Get Item by ID
- **Endpoint**: `/items/{id}`
- **Method**: `GET`
- **Path Parameters**:
  - `id`: The ID of the item to retrieve.

- **Example Request**:
```
GET /items/123
Authorization: Bearer YOUR_API_KEY
```

- **Successful Response**:
```json
{
  "item": {
    "id": 123,
    "name": "Example Item",
    "description": "This is an example item."
  }
}
```

### 3. Create New Item
- **Endpoint**: `/items`
- **Method**: `POST`
- **Request Body**:
```json
{
  "name": "New Item",
  "description": "Description of the new item."
}
```

- **Example Request**:
```
POST /items
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "New Item",
  "description": "Description of the new item."
}
```

- **Successful Response**:
```json
{
  "id": 124,
  "name": "New Item",
  "description": "Description of the new item."
}
```

### 4. Update Item
- **Endpoint**: `/items/{id}`
- **Method**: `PUT`
- **Path Parameters**:
  - `id`: The ID of the item to update.
- **Request Body**:
```json
{
  "name": "Updated Item",
  "description": "Updated description."
}
```

- **Example Request**:
```
PUT /items/123
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "Updated Item",
  "description": "Updated description."
}
```

- **Successful Response**:
```json
{
  "id": 123,
  "name": "Updated Item",
  "description": "Updated description."
}
```

### 5. Delete Item
- **Endpoint**: `/items/{id}`
- **Method**: `DELETE`
- **Path Parameters**:
  - `id`: The ID of the item to delete.

- **Example Request**:
```
DELETE /items/123
Authorization: Bearer YOUR_API_KEY
```

- **Successful Response**:
```json
{
  "message": "Item deleted successfully."
}
```

## Error Handling

Common error responses:
- `400 Bad Request`: Invalid request.
- `401 Unauthorized`: Invalid or missing authentication token.
- `404 Not Found`: Resource not found.
- `500 Internal Server Error`: Unexpected error.

## Contact

For any issues, please contact support at [support@yourservice.com]

# Movie Review API

## Overview
The **Movie Review API** is a Django-based REST API for managing movie reviews. Users can create, retrieve, update, and delete reviews for movies, search for movies, and register or log in to access the API securely.

---

## Endpoints Documentation

### Authentication Endpoints
#### 1. **User Registration**
- **Path**: `/api/register/`
- **Method**: `POST`
- **Description**: Allows users to register by providing a username, password, and optional email.
- **Request Example**:
  ```json
  {
    "username": "newuser",
    "password": "password123",
    "email": "newuser@example.com"
  }
  ```
- **Response Example**:
  ```json
  {
    "message": "User created successfully"
  }
  ```

#### 2. **User Login**
- **Path**: `/api/token/`
- **Method**: `POST`
- **Description**: Allows users to log in and retrieve access and refresh tokens.
- **Request Example**:
  ```json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```
- **Response Example**:
  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
  ```

#### 3. **Token Refresh**
- **Path**: `/api/token/refresh/`
- **Method**: `POST`
- **Description**: Refreshes the access token using the refresh token.
- **Request Example**:
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```
- **Response Example**:
  ```json
  {
    "access": "<new_access_token>"
  }
  ```

---

### Movie Endpoints
#### 1. **List and Create Movies**
- **Path**: `/api/movies/`
- **Method**: `GET`, `POST`
- **Description**:
  - **GET**: Fetches a list of all movies.
  - **POST**: Creates a new movie (Admin only).
- **Request Example (POST)**:
  ```json
  {
    "title": "Inception",
    "genre": "Sci-Fi"
  }
  ```
- **Response Example (GET)**:
  ```json
  [
    {
      "id": 1,
      "title": "Inception",
      "genre": "Sci-Fi"
    }
  ]
  ```

---

### Review Endpoints
#### 1. **List and Create Reviews**
- **Path**: `/api/movies/{movie_id}/reviews/`
- **Method**: `GET`, `POST`
- **Description**:
  - **GET**: Fetches reviews for a specific movie.
  - **POST**: Creates a new review for the specified movie.
- **Request Example (POST)**:
  ```json
  {
    "rating": 5,
    "comment": "Amazing movie!"
  }
  ```
- **Response Example (GET)**:
  ```json
  [
    {
      "id": 1,
      "rating": 5,
      "comment": "Amazing movie!",
      "movie": 1,
      "user": 1
    }
  ]
  ```

---

## Authentication Setup

### Authentication Method
The API uses JSON Web Tokens (JWT) for authentication. Users must log in to receive an access token and a refresh token.

### How to Test Authentication
1. **Register a User**:
   - Send a `POST` request to `/api/register/` with the required user details.
2. **Login**:
   - Send a `POST` request to `/api/token/` with the username and password to receive tokens.
3. **Use the Access Token**:
   - Include the `Authorization` header in subsequent requests:
     ```
     Authorization: Bearer <access_token>
     ```
4. **Refresh the Access Token**:
   - Send a `POST` request to `/api/token/refresh/` with the refresh token.

---

## Notes
- Ensure the API is running locally or deployed on a server.
- Use tools like Postman, curl, or your preferred HTTP client to test the endpoints.

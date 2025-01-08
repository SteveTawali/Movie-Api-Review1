# Movie Review API  

A Django-based API for managing movie reviews.  

## Prerequisites  
- Python 3.8+  
- pip  
- virtualenv  

## Setup Instructions  
1. Clone the repository:  
   ```bash
   git clone <repository_url>
   cd movie_review_api
   ```  

2. Create and activate a virtual environment:  
   ```bash
   virtualenv venv  
   source venv/bin/activate  # On macOS/Linux  
   venv\Scripts\activate  # On Windows  
   ```  

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

4. Run migrations:  
   ```bash
   python manage.py migrate
   ```  

5. Start the development server:  
   ```bash
   python manage.py runserver
   ```  

## Running the API  
Visit `http://127.0.0.1:8000/` in your browser.  

## License  
MIT License  


# Movie Review API

This is a **Movie Review API** built using Django and Django REST Framework (DRF). The API allows users to register, authenticate, and interact with movies and reviews. It provides endpoints for creating, retrieving, updating, and deleting movies and reviews.

---

## Features
- **User Registration and Authentication** using JSON Web Tokens (JWT).
- **Movie Management**: CRUD operations on movies.
- **Review Management**: CRUD operations on movie reviews.
- **Search and Filtering**: Search movies by title and filter reviews by rating or creation date.
- **Pagination**: Efficiently navigate through large sets of data.

---

## Authentication Setup
This API uses **JWT (JSON Web Tokens)** for authentication. Users must obtain a token by logging in and include the token in the `Authorization` header for all protected endpoints.

### Steps to Authenticate
1. **Register a User**:
   Use the `/api/register/` endpoint to create a user by providing a `username`, `password`, and optional `email`.

2. **Obtain a Token**:
   Use the `/api/login/` endpoint with your `username` and `password` to obtain a `refresh` and `access` token.

3. **Include the Token in Headers**:
   Add the `Authorization` header with the format `Bearer <access_token>` to authenticate subsequent requests.

**Example Header**:
```http
Authorization: Bearer your_access_token_here
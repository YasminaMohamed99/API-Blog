# Django Blog Project
This is a Django-based blog application that supports user authentication, CRUD operations for posts and comments, RESTful API development, search and filtering, pagination, and deployment using Docker.

## Table of Contents
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Usage](#api-usage)
- [Testing](#testing)
- [Admin Interface](#admin-interface)

## Features

1. **Models**
    - **Post**: title, content, author (linked to Profile), categories (many-to-many with Category), tags (many-to-many with Tag), created_at, updated_at.
    - **Category**: name, slug.
    - **Tag**: name, slug.
    - **Comment**: post (foreign key to Post), author (linked to Profile), content, created_at.
    - **Profile**: user (one-to-one with Django's User), bio, profile_picture.

2. **User Authentication**
    - User registration, login, logout, and profile management using Django's built-in authentication system.
    - Secure password handling and validation.

3. **CRUD Operations**
    - CRUD operations for Posts and Comments with proper access control.
    - Only authenticated users can create, update, or delete their own posts and comments.

4. **API Development**
    - Doing RESTful API using Django REST Framework for managing posts, categories, tags, and comments.

5. **Search and Filtering**
    - Search functionality to search posts by title and content.
    - Filtering by categories and tags.

6. **Pagination**
    - Pagination for the list of posts in the API.

7. **Admin Interface**
    - Customized Django admin interface to manage posts, categories, tags, comments, and profiles efficiently.

8. **Testing**
    - Created Unit tests and integration tests covering all functionalities of the application.

## Setup Instructions

1. **Clone the Repository**
    ```sh
    git clone https://github.com/YasminaMohamed99/API-Blog.git
    cd API-Blog
    ```

2. **Create a Virtual Environment**
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```
   
4. **Configure PostgreSQL Database**
   - Install PostgreSQL and create a new database and user
   - Add database credential to .env file
       ```sh
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
       ```

5. **Run Migrations**
    ```sh
    python manage.py migrate
    ```

6. **Create a Superuser**
    ```sh
    python manage.py createsuperuser
    ```

7**Run the Development Server**
    ```sh
    python manage.py runserver
    ```

# API Usage

- **Get All Posts**
    ```http
    GET /api/post/
    ```

- **Create a New Post**
    ```http
    POST /api/post/
    Payload =   {
            "id": 15,
            "title": "post_title",
            "content": "content",
            "created_at": "2024-06-28T19:57:16.313014Z",
            "updated_at": "2024-06-28T19:57:16.313014Z",
            "author": 4,
            "categories": [1,2],
            "tags": [1,2]
        }  
    ```

- **Get a Single Post**
    ```http
    GET /api/posts/<id>/
    ```

- **Update a Post**
    ```http
    PUT /api/post/<id>/
    Payload =   {
            "id": 15,
            "title": "post_title",
            "content": "content",
            "created_at": "2024-06-28T19:57:16.313014Z",
            "updated_at": "2024-06-28T19:57:16.313014Z",
            "author": 4,
            "categories": [1,2],
            "tags": [1,2]
        }
    ```

- **Delete a Post**
    ```http
    DELETE /api/posts/<id>/
    ```

- **Get All Categories**
    ```http
    GET /api/categories/
    ```

- **Get All Tags**
    ```http
    GET /api/tags/
    ```

- **Get All Comments**
    ```http
    GET /api/comments/
    ```

- **Create a New Comment**
    ```http
    POST /api/comments/
    Payload = {
        "id": 16,
        "content": "comment",
        "created_at": "2024-06-30T20:20:12.973553Z",
        "updated_at": "2024-06-30T20:20:12.973553Z",
        "author": 5,
        "post": 3
    }
    ```

- **Delete a Comment**
    ```http
    DELETE /api/comments/<id>/
    ```
  
## Testing

   - Run the tests using the following command:
   ```sh
   python manage.py test
   ```

## Admin Interface
   - Access the Django admin interface at /admin/.
   - Use the superuser credentials created during setup to log in.
   - Manage posts, categories, tags, comments, and profiles efficiently through the admin interface.


# Social Forum with REST API

This is a social forum application built with Django and Django REST Framework.  
It provides a RESTful API for users to create posts, upload images, comment on posts, and react to them.

---

## Features

- **User Management**: User registration and authentication.
- **Posts**: Full CRUD (Create, Read, Update, Delete) functionality for posts.
- **Image Uploads**: Attach multiple images to posts with validation for file type and size.
- **Comments**: Add comments to posts.
- **Reactions**: Like or dislike posts.
- **Permissions**: Users can only edit or delete their own posts and comments.
- **Testing**: Unit tests for models and serializers.

---

## Technologies Used

- Django  
- Django REST Framework
- pytest  
- pytest-django

---

## Setup and Installation

### Prerequisites

- Python 3

### Instructions

**1. Clone the repository:**

```bash
git clone <your-repository-url>
cd social_forum
```

**2. Set up the environment and install dependencies**

```bash
make venv
source venv/bin/activate
make install
```

**3. Apply database migrations:**

This will create the necessary tables in your database.

```bash
make db
```

**4. Create a superuser (optional):**

This allows you to access the Django admin panel.

```bash
make superuser
```

**5. Run the development server:**

```bash
make run
```

The application will be available at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Running Tests

To run the unit tests, use the following command:

```bash
make test
```

---

## API Endpoints

### Authentication

- `POST /users/register/` – Register a new user
  **Request Body (JSON):**
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```

### Users

- `GET /users/` – List all users  
- `GET /users/{id}/` – Retrieve a specific user  
- `GET /users/{user_pk}/posts/` – List all posts by a specific user

### Posts

- `GET /posts/` – List all posts  
- `POST /posts/` – Create a new post *(requires authentication)*  
  **Request Body (multipart/form-data):**
  - `title` – *(string)* Post title  
  - `text` – *(string)* Post content  
  - `images` – *(file)* One or more image files *(optional, multiple allowed)*  
- `GET /posts/{id}/` – Retrieve a specific post  
- `PUT /posts/{id}/` – Update a post *(requires ownership)*  
- `DELETE /posts/{id}/` – Delete a post *(requires ownership)*

### Comments

- `GET /posts/{post_pk}/comments/` – List all comments for a post  
- `POST /posts/{post_pk}/comments/` – Add a comment to a post *(requires authentication)*  
- `PUT /posts/{post_pk}/comments/{id}/` – Update a comment *(requires ownership)*  
- `DELETE /posts/{post_pk}/comments/{id}/` – Delete a comment *(requires ownership)*

### Reactions

- `POST /posts/{post_pk}/react/` – Add or update a reaction (like/dislike) to a post *(requires authentication)*  
  **Body:**  
  - `{"type": 1}` – Like  
  - `{"type": -1}` – Dislike

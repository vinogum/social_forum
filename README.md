# Social Forum API

This is a REST API for a social forum application built with Django and Django REST Framework. It provides endpoints for user registration, authentication, and creating posts with images, comments, and reactions.

---

## Features

* **User Management**: Register and authenticate users.
* **Post Management**: Full CRUD (Create, Read, Update, Delete) for posts.
* **Image Uploads**: Attach multiple images to posts.
* **Comments**: Add, view, update, and delete comments on posts.
* **Reactions**: Add, view, update, and delete reactions (likes/dislikes) on posts.
* **Nested Routes**: Access related resources easily (e.g., a user's posts or a post's comments).
* **File Handling**: Automatic cleanup of post directories and images when objects are deleted.

---

## API Endpoints

Here are the main API endpoints available in the project.

### User and Authentication

* `POST /users/register/`: Create a new user.
* `GET /users/`: Get a list of all users.
* `GET /users/{user_id}/`: Get details for a specific user.
* `GET /users/{user_id}/posts/`: Get all posts created by a specific user.

### Posts

* `POST /posts/`: Create a new post.
* `GET /posts/`: Get a list of all posts.
* `GET /posts/{post_id}/`: Get a single post.
* `PATCH /posts/{post_id}/`: Update a post.
* `DELETE /posts/{post_id}/`: Delete a post.

### Comments and Reactions

* `POST /posts/{post_id}/comments/`: Add a comment to a post.
* `GET /posts/{post_id}/comments/`: Get all comments for a post.
* `POST /posts/{post_id}/reactions/`: Add a reaction to a post.
* `GET /posts/{post_id}/reactions/`: Get all reactions for a post.

---

## Getting Started

You can run the project locally or with Docker.

### 1. Run with Docker (Recommended)

This is the easiest way to get the application running.

**Prerequisites:**
* Docker

**Instructions:**
1.  **Build the image:**
    ```sh
    make build
    ```
2.  **Run the container**:
    ```sh
    make run
    ```
    The application will be available at `http://localhost:8000`.

**Note:**  
A superuser is created automatically before the container starts.  
- **Username:** admin  
- **Password:** admin  
- **Email:** admin@example.com

### 2. Run Locally

**Prerequisites:**
* Python 3.10
* pip

**Instructions:**
1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd social-forum
    ```
2.  **Create a virtual environment:**
    ```sh
    make venv
    ```
3.  **Activate the virtual environment:**
    ```sh
    source venv/bin/activate
    ```
4.  **Install dependencies**:
    ```sh
    make install
    ```
5.  **Run database migrations**:
    ```sh
    make db
    ```
6.  **Run the development server**:
    ```sh
    make serve
    ```
    The application will be available at `http://localhost:8000`.

---

## Running Tests

To run the automated tests, set up the project locally and then run the following command:

```sh
pytest

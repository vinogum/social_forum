# Social Forum API

This is a REST API for a social forum application built with Django and Django REST Framework. It provides endpoints for user registration, authentication, and creating posts with images, comments, and reactions.

---

## Features

* [cite_start]**User Management**: Register and authenticate users[cite: 13, 14].
* [cite_start]**Post Management**: Full CRUD (Create, Read, Update, Delete) for posts[cite: 5, 6].
* [cite_start]**Image Uploads**: Attach multiple images to posts[cite: 2].
* [cite_start]**Comments**: Add, view, update, and delete comments on posts[cite: 8].
* [cite_start]**Reactions**: Add, view, update, and delete reactions (likes/dislikes) on posts[cite: 9, 10].
* [cite_start]**Nested Routes**: Access related resources easily (e.g., a user's posts or a post's comments)[cite: 3, 13].
* [cite_start]**File Handling**: Automatic cleanup of post directories and images when objects are deleted[cite: 1, 2].

---

## API Endpoints

Here are the main API endpoints available in the project.

### User and Authentication

* [cite_start]`POST /users/register/`: Create a new user[cite: 13].
* [cite_start]`GET /users/`: Get a list of all users[cite: 13].
* [cite_start]`GET /users/{user_id}/`: Get details for a specific user[cite: 13].
* [cite_start]`GET /users/{user_id}/posts/`: Get all posts created by a specific user[cite: 7, 13].

### Posts

* [cite_start]`POST /posts/`: Create a new post[cite: 3].
* [cite_start]`GET /posts/`: Get a list of all posts[cite: 3, 7].
* [cite_start]`GET /posts/{post_id}/`: Get a single post[cite: 22].
* [cite_start]`PATCH /posts/{post_id}/`: Update a post[cite: 6].
* [cite_start]`DELETE /posts/{post_id}/`: Delete a post[cite: 1].

### Comments and Reactions

* [cite_start]`POST /posts/{post_id}/comments/`: Add a comment to a post[cite: 3, 9].
* [cite_start]`GET /posts/{post_id}/comments/`: Get all comments for a post[cite: 3].
* [cite_start]`POST /posts/{post_id}/reactions/`: Add a reaction to a post[cite: 3, 11].
* [cite_start]`GET /posts/{post_id}/reactions/`: Get all reactions for a post[cite: 3].

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
2.  [cite_start]**Run the container**[cite: 15]:
    ```sh
    make run
    ```
    The application will be available at `http://localhost:8000`.

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
4.  [cite_start]**Install dependencies**[cite: 15]:
    ```sh
    make install
    ```
5.  [cite_start]**Run database migrations**[cite: 15]:
    ```sh
    make db
    ```
6.  [cite_start]**Run the development server**[cite: 15]:
    ```sh
    make serve
    ```
    The application will be available at `http://localhost:8000`.

---

## Running Tests

To run the automated tests, set up the project locally and then run the following command:

```sh
pytest

# Digital Library Management System

This project is a distributed system for managing digital book loans, built with Django and Python, following a microservices architecture.

## System Description

The system is composed of 3 independent microservices:
*   **User Service**: Manages users.
*   **Book Service**: Manages books.
*   **Loan Service**: Manages loans, applying a hexagonal architecture.

## Installation

1.  Clone the repository.
2.  Install the dependencies:
    ```bash
    pip install django djangorestframework requests
    ```

## Usage

1.  Run each microservice in a separate terminal:
    ```bash
    # Terminal 1: User Service
    cd user_service
    python manage.py migrate
    python manage.py runserver 8001

    # Terminal 2: Book Service
    cd book_service
    python manage.py migrate
    python manage.py runserver 8002

    # Terminal 3: Loan Service
    cd loan_service
    python manage.py migrate
    python manage.py runserver 8000
    ```

2.  Use a tool like `curl` or Postman to interact with the APIs:

    *   **Create a user:**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe"}' http://localhost:8001/api/users/
        ```

    *   **Create a book:**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"}' http://localhost:8002/api/books/
        ```

    *   **Create a loan:**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "book_id": 1}' http://localhost:8000/api/loans/
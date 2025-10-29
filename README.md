# Sistema de Gestión de Biblioteca Digital

Este proyecto es un sistema distribuido para gestionar préstamos de libros digitales, construido con Django y Python, siguiendo una arquitectura de microservicios.

## Descripción del Sistema

El sistema se compone de 3 microservicios independientes:
*   **Servicio de Usuarios**: Gestiona los usuarios.
*   **Servicio de Libros**: Gestiona los libros.
*   **Servicio de Préstamos**: Gestiona los préstamos, aplicando una arquitectura hexagonal.

## Instalación

1.  Clona el repositorio.
2.  Instala las dependencias:
    ```bash
    pip install django djangorestframework requests
    ```

## Uso

1.  Ejecuta cada microservicio en una terminal separada:
    ```bash
    # Terminal 1: Servicio de Usuarios
    cd user_service
    python manage.py migrate
    python manage.py runserver 8001

    # Terminal 2: Servicio de Libros
    cd book_service
    python manage.py migrate
    python manage.py runserver 8002

    # Terminal 3: Servicio de Préstamos
    cd loan_service
    python manage.py migrate
    python manage.py runserver 8000
    ```

2.  Usa una herramienta como Postman para interactuar con las APIs.

## Endpoints de la API

A continuación se muestra una lista detallada de todos los endpoints disponibles para cada servicio.

### Servicio de Usuarios (`http://localhost:8001`)

*   **Health Check**
    *   **GET** `/api/health/`
        *   Descripción: Comprueba el estado del servicio.

*   **Usuarios**
    *   **GET** `/api/users/`
        *   Descripción: Recupera una lista de todos los usuarios.
    *   **GET** `/api/users/{id}/`
        *   Descripción: Recupera un usuario específico por ID.
    *   **POST** `/api/users/`
        *   Descripción: Crea un nuevo usuario.
        *   Body: `{"name": "John Doe", "email": "john.doe@example.com"}`
    *   **PUT** `/api/users/{id}/`
        *   Descripción: Actualiza un usuario existente.
        *   Body: `{"name": "Johnathan Doe", "email": "john.doe@email.com"}`
    *   **DELETE** `/api/users/{id}/`
        *   Descripción: Elimina un usuario.

### Servicio de Libros (`http://localhost:8002`)

*   **Health Check**
    *   **GET** `/api/health/`
        *   Descripción: Comprueba el estado del servicio.

*   **Libros**
    *   **GET** `/api/books/`
        *   Descripción: Recupera una lista de todos los libros.
    *   **GET** `/api/books/{id}/`
        *   Descripción: Recupera un libro específico por ID.
    *   **POST** `/api/books/`
        *   Descripción: Crea un nuevo libro.
        *   Body: `{"title": "The Hobbit", "author": "J.R.R. Tolkien"}`
    *   **PUT** `/api/books/{id}/`
        *   Descripción: Actualiza un libro existente.
        *   Body: `{"title": "The Hobbit", "author": "J.R.R. Tolkien"}`
    *   **DELETE** `/api/books/{id}/`
        *   Descripción: Elimina un libro.

### Servicio de Préstamos (`http://localhost:8000`)

*   **Health Check**
    *   **GET** `/api/health/`
        *   Descripción: Comprueba el estado del servicio.

*   **Préstamos**
    *   **GET** `/api/loans/`
        *   Descripción: Recupera una lista de todos los préstamos.
    *   **POST** `/api/loans/`
        *   Descripción: Crea un nuevo préstamo.
        *   Body: `{"user_id": 1, "book_id": 1}`

## Uso con Postman

Puedes usar Postman para interactuar con las APIs. A continuación, se explica cómo puedes configurar las solicitudes:

*   Crea una nueva solicitud en Postman.
*   Establece el método HTTP (por ejemplo, `GET`, `POST`, `PUT`, `DELETE`).
*   Ingresa la URL de la solicitud (por ejemplo, `http://localhost:8001/api/users/`).
*   Para las solicitudes `POST` y `PUT`, ve a la pestaña **Body**, selecciona **raw** y elige **JSON** en el menú desplegable. Luego, ingresa el payload JSON.
*   Haz clic en **Send** para ejecutar la solicitud.
# Sistema de Gestión de Biblioteca Digital

Este proyecto es una implementación de un sistema distribuido para la gestión de préstamos de libros digitales, desarrollado bajo una arquitectura de microservicios.

## ✨ Características

- **Arquitectura de Microservicios:** El sistema está desacoplado en tres servicios independientes: Usuarios, Libros y Préstamos.
- **Arquitectura Hexagonal:** El servicio de Préstamos implementa el patrón de Arquitectura Hexagonal (Puertos y Adaptadores) para un total aislamiento de la lógica de negocio.
- **Contenerización:** Todo el sistema está orquestado con Docker y Docker Compose para un despliegue y desarrollo simplificado.
- **API RESTful:** Cada microservicio expone una API REST para interactuar con sus recursos.

---

## 🏗️ Arquitectura del Sistema

El sistema se compone de los siguientes servicios:

- **Microservicio de Usuarios (`localhost:8000`):** Gestiona la creación y consulta de usuarios.
- **Microservicio de Libros (`localhost:8001`):** Gestiona el catálogo de libros y su estado (disponible, prestado).
- **Microservicio de Préstamos (`localhost:8002`):** Orquesta la lógica de negocio para la creación de préstamos, aplicando reglas como el límite de préstamos por usuario.

---

## 🛠️ Stack Tecnológico

- **Backend:** Python, Django, Django REST Framework
- **Orquestación:** Docker, Docker Compose
- **Bases de Datos:** SQLite (para desarrollo)

---

## 🚀 Puesta en Marcha

Sigue estos pasos para levantar el entorno de desarrollo completo.

### **Prerrequisitos**

Asegúrate de tener instaladas las siguientes herramientas en tu sistema:
- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### **Instalación y Ejecución**

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    ```

2.  **Navega al directorio del proyecto:**
    ```bash
    cd biblioteca_digital
    ```

3.  **Levanta los servicios con Docker Compose:**
    Este comando construirá las imágenes de los contenedores (si es la primera vez) y los iniciará.
    ```bash
    docker-compose up --build
    ```

Una vez finalizado el proceso, los tres servicios estarán corriendo y accesibles en sus respectivos puertos.

---

## ⚙️ Endpoints de la API

A continuación se detallan los endpoints disponibles para cada servicio.

### **API de Usuarios (Port: 8000)**

| Método | URL                  | Body (JSON)                                | Resultado                               |
|--------|----------------------|--------------------------------------------|-----------------------------------------|
| `POST` | `/api/users/`        | `{"name": "...", "email": "..."}`          | `201 Created` - Crea un nuevo usuario.  |
| `GET`  | `/api/users/`        | N/A                                        | `200 OK` - Devuelve la lista de usuarios. |

### **API de Libros (Port: 8001)**

| Método  | URL                | Body (JSON)                         | Resultado                                      |
|---------|--------------------|-------------------------------------|------------------------------------------------|
| `POST`  | `/api/books/`      | `{"title": "...", "author": "..."}` | `201 Created` - Crea un nuevo libro.         |
| `GET`   | `/api/books/`      | N/A                                 | `200 OK` - Devuelve la lista de libros.      |
| `PATCH` | `/api/books/1/`    | `{"status": "prestado"}`            | `200 OK` - Actualiza parcialmente un libro.    |

### **API de Préstamos (Port: 8002)**

| Método | URL           | Body (JSON)                         | Resultado                                                           |
|--------|---------------|-------------------------------------|---------------------------------------------------------------------|
| `POST` | `/api/loans/` | `{"user_id": 1, "book_id": 1}`      | `201 Created` - Crea un nuevo préstamo si se cumplen las reglas.    |
| `POST` | `/api/loans/` | `{"user_id": 1, "book_id": 2}`      | `400 Bad Request` - Si el usuario excede el límite de 3 préstamos.    |

---

## 🧪 Pruebas con Postman

<img width="1806" height="846" alt="Captura de pantalla 2025-10-27 132509" src="https://github.com/user-attachments/assets/351f8786-9f75-4aa1-8101-faeaebbcf7ae" />
<img width="1<img width="1810" height="882" alt="Captura de pantalla 2025-10-27 134401" src="https://github.com/user-attachments/assets/e807949c-ff93-492d-b4c7-50e655faa240" />
<img width="1810" height="882" alt="Captura de pantalla 2025-10-27 134401" src="https://github.com/user-attachments/assets/618cb072-810c-40ad-b936-0a86a5f3e6b6" />
<img width="868" height="737" alt="Captura de pantalla 2025-10-27 134856" src="https://github.com/user-attachments/assets/b9d1104d-0cdc-4a12-8510-aaf32a1d1610" />

Tras realizar 3 préstamos exitosos para el mismo usuario, se intenta realizar un cuarto. El sistema lo rechaza correctamente, devolviendo un error `400 Bad Request` y el mensaje correspondiente, validando la lógica de negocio implementada en el dominio.

# Frontend del Sistema de Biblioteca

Este directorio contiene el frontend para interactuar con los microservicios de gestión de una biblioteca. La interfaz permite visualizar y gestionar usuarios, libros y préstamos.

## Descripción General

El frontend es una aplicación web de una sola página (SPA) construida con HTML, CSS y JavaScript puros. Se comunica con los tres microservicios (Usuarios, Libros y Préstamos) a través de peticiones HTTP (AJAX) para obtener y enviar datos.

## Archivos

-   `index.html`: Es el punto de entrada de la aplicación. Contiene la estructura HTML de la página, incluyendo los botones para cargar datos, las listas para mostrar la información y el formulario para crear nuevos préstamos.
-   `style.css`: Contiene las reglas de estilo para dar una apariencia visual agradable y organizada a la interfaz.
-   `script.js`: Contiene toda la lógica de la aplicación. Se encarga de:
    -   Manejar los eventos de los botones (Cargar Usuarios, Cargar Libros, Cargar Préstamos).
    -   Realizar peticiones `fetch` a los endpoints de los microservicios.
    -   Actualizar dinámicamente el DOM para mostrar los datos recibidos.
    -   Gestionar el envío del formulario para crear un nuevo préstamo.

## Cómo Usar

1.  **Asegúrate de que los microservicios estén en ejecución**:
    -   Servicio de Usuarios: `http://localhost:8001`
    -   Servicio de Libros: `http://localhost:8002`
    -   Servicio de Préstamos: `http://localhost:8000`

2.  **Abrir el frontend**:
    -   Simplemente abre el archivo `index.html` en tu navegador web. No se requiere un servidor web para el frontend, ya que es estático.

## Interacción con Microservicios

El archivo `script.js` define las URLs de los microservicios y las utiliza para realizar las siguientes operaciones:

-   **Cargar Usuarios**: Al hacer clic en "Cargar Usuarios", se realiza una petición `GET` a `http://localhost:8001/users/` y se muestra la lista de usuarios.
-   **Cargar Libros**: Al hacer clic en "Cargar Libros", se realiza una petición `GET` a `http://localhost:8002/books/` y se muestra la lista de libros.
-   **Cargar Préstamos**: Al hacer clic en "Cargar Préstamos", se realiza una petición `GET` a `http://localhost:8000/loans/` y se muestra la lista de préstamos.
-   **Crear Préstamo**: Al rellenar el formulario y hacer clic en "Crear Préstamo", se realiza una petición `POST` a `http://localhost:8000/loans/` con el `user_id` y el `book_id` para registrar un nuevo préstamo.

Debido a la política de Same-Origin Policy (CORS) de los navegadores, es posible que necesites configurar los microservicios de Django para que acepten peticiones desde el origen del frontend (que al ser un archivo local, puede ser `null` o `file://`). Esto generalmente se soluciona instalando y configurando `django-cors-headers` en cada uno de los proyectos de Django.
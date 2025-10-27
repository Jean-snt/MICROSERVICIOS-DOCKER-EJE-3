# MICROSERVICIOS-DOCKER-EJE-3
EJERCICIO PRÁCTICO: ARQUITECTURA HEXAGONAL Y MICROSERVICIOS
Título: Sistema de Gestión de Biblioteca Digital
Nivel: Básico
Tecnologías: Django, Python, Microservicios	

1. CONTEXTO Y OBJETIVO
Una biblioteca digital necesita modernizar su sistema de préstamos. Debes desarrollar una plataforma distribuida que gestione préstamos de libros digitales aplicando arquitectura hexagonal en el componente principal.

2. DESCRIPCIÓN DEL SISTEMA
El sistema estará compuesto por 3 microservicios independientes:
Microservicio de Préstamos (desarrollo principal)
Microservicio de Libros
Microservicio de Usuarios

3. REQUISITOS FUNCIONALES
3.1 Flujo Principal de Préstamos:
Usuario solicita préstamo de un libro
Validar que el usuario existe y está activo
Verificar que el libro existe y está disponible
Registrar el préstamo con fechas de inicio y vencimiento
Actualizar estado del libro a "prestado"
3.2 Reglas de Negocio:
Límite de 3 préstamos activos por usuario
Duración máxima de préstamo: 15 días
Usuarios suspendidos no pueden pedir préstamos
Libros eliminados no están disponibles

4. REQUISITOS TÉCNICOS
4.1 Microservicio de Préstamos:
Implementar con arquitectura hexagonal en Django
Aislamiento completo del dominio de negocio
Definición clara de puertos y adaptadores
Independencia de frameworks externos
4.2 Comunicación entre Microservicios:
Comunicación HTTP/REST entre servicios
Base de datos independiente por microservicio
Manejo apropiado de fallos en comunicación

5. ENTREGABLES
Código fuente del Microservicio de Préstamos con arquitectura hexagonal
Microservicio de Libros funcional
Microservicio de Usuarios funcional
Comunicación demostrada entre los 3 servicios
Documentación básica de instalación y uso


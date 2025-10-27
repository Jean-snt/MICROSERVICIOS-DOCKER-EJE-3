#!/bin/bash

echo "=== Cargando datos de prueba para el Sistema de Biblioteca Digital ==="

# Esperar a que los servicios estén listos
echo "Esperando a que los servicios estén listos..."
sleep 10

# Crear usuarios de prueba
echo "Creando usuarios de prueba..."

curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan Pérez", "email": "juan@example.com", "status": "active"}' \
  -w "\nStatus: %{http_code}\n\n"

curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "María García", "email": "maria@example.com", "status": "active"}' \
  -w "\nStatus: %{http_code}\n\n"

curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Carlos López", "email": "carlos@example.com", "status": "suspended"}' \
  -w "\nStatus: %{http_code}\n\n"

# Crear libros de prueba
echo "Creando libros de prueba..."

curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Python para Principiantes", "author": "Autor Python", "isbn": "1234567890123", "description": "Libro introductorio de Python"}' \
  -w "\nStatus: %{http_code}\n\n"

curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Django Avanzado", "author": "Autor Django", "isbn": "1234567890124", "description": "Guía avanzada de Django"}' \
  -w "\nStatus: %{http_code}\n\n"

curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Arquitectura de Software", "author": "Autor Arquitectura", "isbn": "1234567890125", "description": "Patrones y arquitecturas de software"}' \
  -w "\nStatus: %{http_code}\n\n"

curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Microservicios", "author": "Autor Microservicios", "isbn": "1234567890126", "description": "Diseño de microservicios"}' \
  -w "\nStatus: %{http_code}\n\n"

curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Libro Eliminado", "author": "Autor Eliminado", "isbn": "1234567890127", "description": "Este libro será eliminado"}' \
  -w "\nStatus: %{http_code}\n\n"

# Eliminar el último libro para probar la funcionalidad
echo "Eliminando libro de prueba..."
curl -X POST http://localhost:8002/api/books/5/delete_book/ \
  -w "\nStatus: %{http_code}\n\n"

echo "=== Datos de prueba cargados exitosamente ==="
echo ""
echo "Usuarios creados:"
echo "- Juan Pérez (ID: 1) - Activo"
echo "- María García (ID: 2) - Activo" 
echo "- Carlos López (ID: 3) - Suspendido"
echo ""
echo "Libros creados:"
echo "- Python para Principiantes (ID: 1) - Disponible"
echo "- Django Avanzado (ID: 2) - Disponible"
echo "- Arquitectura de Software (ID: 3) - Disponible"
echo "- Microservicios (ID: 4) - Disponible"
echo "- Libro Eliminado (ID: 5) - Eliminado"
echo ""
echo "Puedes probar el sistema con los siguientes comandos:"
echo ""
echo "# Verificar si Juan puede pedir préstamo:"
echo "curl http://localhost:8003/api/loans/check_user_can_borrow/?user_id=1"
echo ""
echo "# Crear un préstamo:"
echo "curl -X POST http://localhost:8003/api/loans/ -H 'Content-Type: application/json' -d '{\"user_id\": 1, \"book_id\": 1}'"
echo ""
echo "# Ver préstamos activos de Juan:"
echo "curl http://localhost:8003/api/loans/user_active_loans/?user_id=1"
echo ""
echo "# Intentar préstamo con usuario suspendido (debería fallar):"
echo "curl -X POST http://localhost:8003/api/loans/ -H 'Content-Type: application/json' -d '{\"user_id\": 3, \"book_id\": 2}'"

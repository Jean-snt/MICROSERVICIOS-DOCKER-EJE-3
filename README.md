# Sistema de Gestión de Biblioteca Digital
## Arquitectura Hexagonal y Microservicios

### Descripción del Proyecto

Este proyecto implementa un sistema de gestión de préstamos de libros digitales utilizando **Arquitectura Hexagonal** (Ports and Adapters) en el microservicio principal de préstamos, junto con una arquitectura de **microservicios** distribuidos.

### Arquitectura del Sistema

El sistema está compuesto por **3 microservicios independientes**:

1. **Microservicio de Usuarios** (Puerto 8001)
   - Gestiona usuarios del sistema
   - Estados: activo, suspendido, inactivo

2. **Microservicio de Libros** (Puerto 8002)
   - Gestiona el catálogo de libros
   - Estados: disponible, prestado, eliminado

3. **Microservicio de Préstamos** (Puerto 8003) - **ARQUITECTURA HEXAGONAL**
   - Gestiona préstamos de libros
   - Implementa todas las reglas de negocio
   - Comunicación con otros microservicios

### Arquitectura Hexagonal en el Microservicio de Préstamos

#### Componentes Principales:

**1. Dominio (Domain Layer)**
- `entities.py`: Entidades de negocio (User, Book, Loan, LoanDomainService)
- `ports.py`: Interfaces (puertos) que definen contratos

**2. Adaptadores (Adapters Layer)**
- `external_services.py`: Adaptadores para servicios externos (HTTP)
- `repositories.py`: Adaptadores para persistencia (Django ORM)

**3. Aplicación (Application Layer)**
- `loan_use_case.py`: Casos de uso que orquestan la lógica de negocio

**4. Infraestructura (Infrastructure Layer)**
- Django REST Framework
- PostgreSQL
- Docker

### Reglas de Negocio Implementadas

1. **Límite de préstamos**: Máximo 3 préstamos activos por usuario
2. **Duración**: Préstamos por 15 días máximo
3. **Usuarios suspendidos**: No pueden pedir préstamos
4. **Libros eliminados**: No están disponibles para préstamo
5. **Validaciones**: Usuario y libro deben existir y estar activos

### Tecnologías Utilizadas

- **Backend**: Django 4.2.7 + Django REST Framework
- **Base de datos**: PostgreSQL (una por microservicio)
- **Contenedores**: Docker + Docker Compose
- **Comunicación**: HTTP/REST entre microservicios
- **Arquitectura**: Hexagonal (Ports and Adapters)

### Estructura del Proyecto

```
MICROSERVICIOS-DOCKER-EJE-3/
├── docker-compose.yml
├── users-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── users_project/
│   └── users/
├── books-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── books_project/
│   └── books/
└── loans-service/
    ├── Dockerfile
    ├── requirements.txt
    ├── loans_project/
    ├── domain/
    │   ├── entities.py
    │   └── ports.py
    ├── adapters/
    │   ├── external_services.py
    │   └── repositories.py
    ├── application/
    │   └── loan_use_case.py
    └── loans/
```

### Instalación y Ejecución

#### Prerrequisitos
- Docker
- Docker Compose

#### Comandos de Ejecución Paso a Paso

**1. Clonar o descargar el proyecto**
```bash
# Navegar al directorio del proyecto
cd MICROSERVICIOS-DOCKER-EJE-3
```

**2. Construir y ejecutar todos los servicios**
```bash
# Construir las imágenes Docker
docker-compose build

# Ejecutar todos los servicios
docker-compose up -d
```

**3. Verificar que todos los servicios estén ejecutándose**
```bash
# Ver el estado de los contenedores
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs users-service
docker-compose logs books-service
docker-compose logs loans-service
```

**4. Ejecutar migraciones de base de datos**
```bash
# Migraciones para usuarios
docker-compose exec users-service python manage.py migrate

# Migraciones para libros
docker-compose exec books-service python manage.py migrate

# Migraciones para préstamos
docker-compose exec loans-service python manage.py migrate
```

**5. Crear superusuarios (opcional)**
```bash
# Superusuario para usuarios
docker-compose exec users-service python manage.py createsuperuser

# Superusuario para libros
docker-compose exec books-service python manage.py createsuperuser

# Superusuario para préstamos
docker-compose exec loans-service python manage.py createsuperuser
```

**6. Cargar datos de prueba (opcional)**
```bash
# Crear usuarios de prueba
curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan Pérez", "email": "juan@example.com", "status": "active"}'

curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "María García", "email": "maria@example.com", "status": "active"}'

# Crear libros de prueba
curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Python para Principiantes", "author": "Autor Python", "isbn": "1234567890123", "description": "Libro introductorio de Python"}'

curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Django Avanzado", "author": "Autor Django", "isbn": "1234567890124", "description": "Guía avanzada de Django"}'
```

### URLs de los Servicios

- **Usuarios**: http://localhost:8001/api/users/
- **Libros**: http://localhost:8002/api/books/
- **Préstamos**: http://localhost:8003/api/loans/

### Endpoints de Salud (Health Check)

Todos los microservicios incluyen un endpoint `/healthz` para verificar su estado de salud:

- **Usuarios Health**: http://localhost:8001/healthz/
- **Libros Health**: http://localhost:8002/healthz/
- **Préstamos Health**: http://localhost:8003/healthz/

**Respuesta del endpoint de salud:**
```json
{
    "status": "healthy",
    "service": "nombre-del-servicio",
    "timestamp": "N/A"
}
```

**Verificar estado de todos los servicios:**
```bash
# Verificar usuarios
curl http://localhost:8001/healthz/

# Verificar libros
curl http://localhost:8002/healthz/

# Verificar préstamos
curl http://localhost:8003/healthz/
```

### Endpoints Principales

#### Microservicio de Usuarios (8001)
- `GET /api/users/` - Listar usuarios
- `POST /api/users/` - Crear usuario
- `GET /api/users/{id}/` - Obtener usuario
- `GET /api/users/{id}/check_status/` - Verificar estado
- `GET /healthz/` - Health check del servicio

#### Microservicio de Libros (8002)
- `GET /api/books/` - Listar libros
- `POST /api/books/` - Crear libro
- `GET /api/books/{id}/` - Obtener libro
- `GET /api/books/{id}/check_availability/` - Verificar disponibilidad
- `GET /healthz/` - Health check del servicio

#### Microservicio de Préstamos (8003) - Arquitectura Hexagonal
- `GET /api/loans/` - Listar préstamos
- `POST /api/loans/` - Crear préstamo
- `GET /api/loans/{id}/` - Obtener préstamo
- `POST /api/loans/{id}/return_loan/` - Devolver préstamo
- `GET /api/loans/user_active_loans/?user_id={id}` - Préstamos activos del usuario
- `GET /api/loans/active_loans/` - Todos los préstamos activos
- `GET /api/loans/check_user_can_borrow/?user_id={id}` - Verificar si puede pedir préstamo
- `GET /api/loans/check_book_availability/?book_id={id}` - Verificar disponibilidad del libro
- `GET /healthz/` - Health check del servicio

### Ejemplos de Uso

#### 1. Verificar estado de salud de los servicios
```bash
# Verificar usuarios
curl http://localhost:8001/healthz/

# Verificar libros
curl http://localhost:8002/healthz/

# Verificar préstamos
curl http://localhost:8003/healthz/
```

#### 2. Crear un préstamo
```bash
curl -X POST http://localhost:8003/api/loans/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "book_id": 1}'
```

#### 3. Verificar si un usuario puede pedir préstamo
```bash
curl http://localhost:8003/api/loans/check_user_can_borrow/?user_id=1
```

#### 4. Verificar disponibilidad de un libro
```bash
curl http://localhost:8003/api/loans/check_book_availability/?book_id=1
```

#### 5. Devolver un préstamo
```bash
curl -X POST http://localhost:8003/api/loans/1/return_loan/
```

#### 6. Ver préstamos activos de un usuario
```bash
curl http://localhost:8003/api/loans/user_active_loans/?user_id=1
```

### Comandos de Mantenimiento

#### Parar servicios
```bash
docker-compose down
```

#### Parar y eliminar volúmenes
```bash
docker-compose down -v
```

#### Reconstruir un servicio específico
```bash
docker-compose build users-service
docker-compose up -d users-service
```

#### Ver logs en tiempo real
```bash
docker-compose logs -f loans-service
```

#### Acceder al shell de un contenedor
```bash
docker-compose exec loans-service bash
```

### Ventajas de la Arquitectura Hexagonal

1. **Aislamiento del Dominio**: La lógica de negocio está completamente separada de la infraestructura
2. **Testabilidad**: Fácil de probar con mocks de los adaptadores
3. **Flexibilidad**: Cambiar implementaciones sin afectar el dominio
4. **Independencia**: El dominio no depende de frameworks externos
5. **Mantenibilidad**: Código más limpio y organizado

### Consideraciones de Producción

- Configurar variables de entorno para URLs de servicios
- Implementar autenticación y autorización
- Agregar logging y monitoreo
- Configurar bases de datos con credenciales seguras
- Implementar circuit breakers para comunicación entre servicios
- Agregar tests unitarios y de integración

### Troubleshooting

#### Si un servicio no inicia:
```bash
# Ver logs específicos
docker-compose logs [nombre-servicio]

# Reiniciar servicio
docker-compose restart [nombre-servicio]
```

#### Si hay problemas de conectividad:
```bash
# Verificar que las bases de datos estén ejecutándose
docker-compose ps

# Verificar conectividad entre servicios
docker-compose exec loans-service ping users-service
```

#### Si hay errores de migración:
```bash
# Ejecutar migraciones manualmente
docker-compose exec [servicio] python manage.py migrate
```

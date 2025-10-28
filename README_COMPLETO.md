# 📚 Sistema de Gestión de Biblioteca Digital
## Arquitectura Hexagonal y Microservicios

### 🎯 Descripción del Proyecto

Este proyecto implementa un **Sistema de Gestión de Biblioteca Digital** utilizando **Arquitectura Hexagonal** (Ports and Adapters) en el microservicio principal de préstamos, junto con una arquitectura de **microservicios distribuidos**.
.
### 🏗️ Arquitectura del Sistema

El sistema está compuesto por **3 microservicios independientes**:

| Microservicio | Puerto | Descripción | Base de Datos |
|---------------|--------|-------------|---------------|
| **Usuarios** | 8001 | Gestión de usuarios del sistema | PostgreSQL (Puerto 5432) |
| **Libros** | 8002 | Catálogo de libros digitales | PostgreSQL (Puerto 5433) |
| **Préstamos** | 8003 | Gestión de préstamos (**ARQUITECTURA HEXAGONAL**) | PostgreSQL (Puerto 5434) |

### 🔧 Arquitectura Hexagonal en el Microservicio de Préstamos

#### Componentes Principales:

**1. Dominio (Domain Layer)**
- `entities.py`: Entidades de negocio puras (User, Book, Loan, LoanDomainService)
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

### 📋 Reglas de Negocio Implementadas

1. **Límite de préstamos**: Máximo 3 préstamos activos por usuario
2. **Duración**: Préstamos por 15 días máximo
3. **Usuarios suspendidos**: No pueden pedir préstamos
4. **Libros eliminados**: No están disponibles para préstamo
5. **Validaciones**: Usuario y libro deben existir y estar activos
6. **Comunicación**: Sincronización automática entre microservicios

### 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2.7 + Django REST Framework
- **Base de datos**: PostgreSQL (una por microservicio)
- **Contenedores**: Docker + Docker Compose
- **Comunicación**: HTTP/REST entre microservicios
- **Arquitectura**: Hexagonal (Ports and Adapters)

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Docker Desktop instalado y ejecutándose
- Docker Compose

### Comandos de Ejecución Paso a Paso

#### 1. **Clonar o descargar el proyecto**
```bash
# Navegar al directorio del proyecto
cd MICROSERVICIOS-DOCKER-EJE-3
```

#### 2. **Construir y ejecutar todos los servicios**
```bash
# Construir las imágenes Docker
docker-compose build

# Ejecutar todos los servicios
docker-compose up -d
```

#### 3. **Verificar que todos los servicios estén ejecutándose**
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

#### 4. **Ejecutar migraciones de base de datos**
```bash
# Migraciones para usuarios
docker-compose exec users-service python manage.py migrate

# Migraciones para libros
docker-compose exec books-service python manage.py migrate

# Migraciones para préstamos
docker-compose exec loans-service python manage.py migrate
```

#### 5. **Cargar datos de prueba**
```bash
# En Windows PowerShell
powershell -ExecutionPolicy Bypass -File .\load_test_data.ps1

# En Linux/Mac
bash load_test_data.sh
```

---

## 🌐 URLs de los Servicios

### **Microservicio de Usuarios** (Puerto 8001)
- **Página de Inicio**: `http://localhost:8001` ✅ (Muestra información del servicio)
- **API Base**: `http://localhost:8001/api/users/`
- **Admin**: `http://localhost:8001/admin/`

### **Microservicio de Libros** (Puerto 8002)
- **Página de Inicio**: `http://localhost:8002` ✅ (Muestra información del servicio)
- **API Base**: `http://localhost:8002/api/books/`
- **Admin**: `http://localhost:8002/admin/`

### **Microservicio de Préstamos** (Puerto 8003) - **ARQUITECTURA HEXAGONAL**
- **Página de Inicio**: `http://localhost:8003` ✅ (Muestra información del servicio y reglas de negocio)
- **API Base**: `http://localhost:8003/api/loans/`
- **Admin**: `http://localhost:8003/admin/`

### **📋 Información que muestran las páginas de inicio:**

**Usuarios** (`http://localhost:8001`):
```json
{
  "service": "Microservicio de Usuarios",
  "version": "1.0.0",
  "description": "Gestión de usuarios del sistema de biblioteca digital",
  "endpoints": {
    "users": "/api/users/",
    "admin": "/admin/"
  },
  "status": "running"
}
```

**Libros** (`http://localhost:8002`):
```json
{
  "service": "Microservicio de Libros",
  "version": "1.0.0",
  "description": "Catálogo de libros digitales del sistema de biblioteca",
  "endpoints": {
    "books": "/api/books/",
    "admin": "/admin/"
  },
  "status": "running"
}
```

**Préstamos** (`http://localhost:8003`):
```json
{
  "service": "Microservicio de Préstamos",
  "version": "1.0.0",
  "description": "Gestión de préstamos con Arquitectura Hexagonal",
  "architecture": "Hexagonal (Ports and Adapters)",
  "endpoints": {
    "loans": "/api/loans/",
    "admin": "/admin/"
  },
  "business_rules": [
    "Máximo 3 préstamos activos por usuario",
    "Préstamos por 15 días",
    "Usuarios suspendidos no pueden pedir préstamos",
    "Libros eliminados no están disponibles"
  ],
  "status": "running"
}
```

---

## 🔐 Panel de Administración (Django Admin)

### **👑 Credenciales de Superusuario**

Para acceder a los paneles de administración de cada microservicio, utiliza las siguientes credenciales:

| Campo | Valor |
|-------|-------|
| **Nombre de usuario** | `biblioteca_admin` |
| **Contraseña** | `admin123` |

### **🌐 URLs del Panel de Administración**

| Microservicio | URL del Admin | Descripción |
|---------------|---------------|-------------|
| **👥 Usuarios** | `http://localhost:8001/admin/` | Gestión de usuarios del sistema |
| **📚 Libros** | `http://localhost:8002/admin/` | Gestión del catálogo de libros |
| **📖 Préstamos** | `http://localhost:8003/admin/` | Gestión de préstamos y devoluciones |

### **📝 Instrucciones de Acceso**

1. **Abre tu navegador web**
2. **Navega a cualquiera de las URLs del admin** (ej: `http://localhost:8001/admin/`)
3. **En el formulario de login:**
   - **Campo "Nombre de usuario"**: `biblioteca_admin`
   - **Campo "Contraseña"**: `admin123`
4. **Haz clic en "Iniciar sesión"**

### **✨ Funcionalidades del Panel de Administración**

**En cada panel puedes:**
- ✅ **Ver todos los registros** de la base de datos
- ✅ **Crear nuevos registros** (usuarios, libros, préstamos)
- ✅ **Editar registros existentes**
- ✅ **Eliminar registros** (con confirmación)
- ✅ **Buscar y filtrar** registros
- ✅ **Ver estadísticas** y conteos
- ✅ **Exportar datos** en diferentes formatos

### **🔧 Credenciales Alternativas**

Si prefieres usar las credenciales originales:

| Campo | Valor |
|-------|-------|
| **Nombre de usuario** | `admin` |
| **Contraseña** | `admin123` |

### **⚠️ Notas Importantes**

- **Django usa "Nombre de usuario"** para la autenticación, no el email
- **Las credenciales son sensibles a mayúsculas**
- **Cada microservicio tiene su propio panel de administración independiente**
- **Los cambios se reflejan inmediatamente en las APIs REST**

---

## 📡 Endpoints Disponibles

### 🔹 Microservicio de Usuarios (8001)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/users/` | Listar todos los usuarios |
| `POST` | `/api/users/` | Crear nuevo usuario |
| `GET` | `/api/users/{id}/` | Obtener usuario por ID |
| `PUT` | `/api/users/{id}/` | Actualizar usuario |
| `DELETE` | `/api/users/{id}/` | Eliminar usuario |
| `GET` | `/api/users/{id}/check_status/` | Verificar estado del usuario |

**Ejemplo de creación de usuario:**
```json
POST http://localhost:8001/api/users/
{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "status": "active"
}
```

### 🔹 Microservicio de Libros (8002)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/books/` | Listar todos los libros |
| `POST` | `/api/books/` | Crear nuevo libro |
| `GET` | `/api/books/{id}/` | Obtener libro por ID |
| `PUT` | `/api/books/{id}/` | Actualizar libro |
| `DELETE` | `/api/books/{id}/` | Eliminar libro |
| `GET` | `/api/books/{id}/check_availability/` | Verificar disponibilidad |
| `POST` | `/api/books/{id}/mark_as_loaned/` | Marcar como prestado |
| `POST` | `/api/books/{id}/mark_as_available/` | Marcar como disponible |
| `POST` | `/api/books/{id}/delete_book/` | Eliminar libro (soft delete) |

**Ejemplo de creación de libro:**
```json
POST http://localhost:8002/api/books/
{
    "title": "Python para Principiantes",
    "author": "Autor Python",
    "isbn": "1234567890123",
    "description": "Libro introductorio de Python"
}
```

### 🔹 Microservicio de Préstamos (8003) - **ARQUITECTURA HEXAGONAL**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/loans/` | Listar todos los préstamos |
| `POST` | `/api/loans/` | Crear nuevo préstamo |
| `GET` | `/api/loans/{id}/` | Obtener préstamo por ID |
| `PUT` | `/api/loans/{id}/` | Actualizar préstamo |
| `DELETE` | `/api/loans/{id}/` | Eliminar préstamo |
| `POST` | `/api/loans/{id}/return_loan/` | Devolver préstamo |
| `GET` | `/api/loans/user_active_loans/?user_id={id}` | Préstamos activos del usuario |
| `GET` | `/api/loans/active_loans/` | Todos los préstamos activos |
| `GET` | `/api/loans/check_user_can_borrow/?user_id={id}` | Verificar si puede pedir préstamo |
| `GET` | `/api/loans/check_book_availability/?book_id={id}` | Verificar disponibilidad del libro |

**Ejemplo de creación de préstamo:**
```json
POST http://localhost:8003/api/loans/
{
    "user_id": 1,
    "book_id": 1
}
```

---

## 🧪 Ejemplos de Uso con URLs Completas

### **1. Verificar servicios**
```bash
# Verificar páginas de inicio de los servicios
curl http://localhost:8001
curl http://localhost:8002
curl http://localhost:8003

# Verificar APIs de los servicios
curl http://localhost:8001/api/users/
curl http://localhost:8002/api/books/
curl http://localhost:8003/api/loans/
```

### **2. Crear usuarios de prueba**
```bash
# Usuario activo
curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan Pérez", "email": "juan@example.com", "status": "active"}'

# Usuario suspendido
curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Carlos López", "email": "carlos@example.com", "status": "suspended"}'
```

### **3. Crear libros de prueba**
```bash
# Libro disponible
curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Python para Principiantes", "author": "Autor Python", "isbn": "1234567890123", "description": "Libro introductorio de Python"}'

# Libro disponible
curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Django Avanzado", "author": "Autor Django", "isbn": "1234567890124", "description": "Guía avanzada de Django"}'
```

### **4. Probar funcionalidades del sistema de préstamos**

#### **Verificar si un usuario puede pedir préstamo:**
```bash
curl http://localhost:8003/api/loans/check_user_can_borrow/?user_id=1
```

#### **Crear un préstamo:**
```bash
curl -X POST http://localhost:8003/api/loans/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "book_id": 1}'
```

#### **Ver préstamos activos de un usuario:**
```bash
curl http://localhost:8003/api/loans/user_active_loans/?user_id=1
```

#### **Ver todos los préstamos activos:**
```bash
curl http://localhost:8003/api/loans/active_loans/
```

#### **Devolver un préstamo:**
```bash
curl -X POST http://localhost:8003/api/loans/1/return_loan/
```

#### **Verificar disponibilidad de un libro:**
```bash
curl http://localhost:8003/api/loans/check_book_availability/?book_id=1
```

### **5. Probar reglas de negocio**

#### **Intentar préstamo con usuario suspendido (debería fallar):**
```bash
curl -X POST http://localhost:8003/api/loans/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3, "book_id": 2}'
```

#### **Intentar préstamo con libro eliminado (debería fallar):**
```bash
curl -X POST http://localhost:8003/api/loans/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "book_id": 5}'
```

---

## 🔧 Comandos de Mantenimiento

### **Parar servicios**
```bash
docker-compose down
```

### **Parar y eliminar volúmenes**
```bash
docker-compose down -v
```

### **Reconstruir un servicio específico**
```bash
docker-compose build users-service
docker-compose up -d users-service
```

### **Ver logs en tiempo real**
```bash
docker-compose logs -f loans-service
```

### **Acceder al shell de un contenedor**
```bash
docker-compose exec loans-service bash
```

### **Ejecutar comandos Django**
```bash
# Crear superusuario (si no existe)
docker-compose exec users-service python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('biblioteca_admin', 'biblioteca@admin.com', 'admin123') if not User.objects.filter(username='biblioteca_admin').exists() else print('Superusuario ya existe')"

docker-compose exec books-service python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('biblioteca_admin', 'biblioteca@admin.com', 'admin123') if not User.objects.filter(username='biblioteca_admin').exists() else print('Superusuario ya existe')"

docker-compose exec loans-service python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('biblioteca_admin', 'biblioteca@admin.com', 'admin123') if not User.objects.filter(username='biblioteca_admin').exists() else print('Superusuario ya existe')"

# Ejecutar migraciones
docker-compose exec users-service python manage.py migrate
docker-compose exec books-service python manage.py migrate
docker-compose exec loans-service python manage.py migrate
```

### **🔐 Credenciales de Administrador**
- **Usuario**: `biblioteca_admin`
- **Contraseña**: `admin123`
- **URLs Admin**: 
  - Usuarios: `http://localhost:8001/admin/`
  - Libros: `http://localhost:8002/admin/`
  - Préstamos: `http://localhost:8003/admin/`

---

## 🎯 Ventajas de la Arquitectura Hexagonal

1. **Aislamiento del Dominio**: La lógica de negocio está completamente separada de la infraestructura
2. **Testabilidad**: Fácil de probar con mocks de los adaptadores
3. **Flexibilidad**: Cambiar implementaciones sin afectar el dominio
4. **Independencia**: El dominio no depende de frameworks externos
5. **Mantenibilidad**: Código más limpio y organizado
6. **Escalabilidad**: Fácil agregar nuevos adaptadores o casos de uso

---

## 🐛 Troubleshooting

### **Si un servicio no inicia:**
```bash
# Ver logs específicos
docker-compose logs [nombre-servicio]

# Reiniciar servicio
docker-compose restart [nombre-servicio]
```

### **Si hay problemas de conectividad:**
```bash
# Verificar que las bases de datos estén ejecutándose
docker-compose ps

# Verificar conectividad entre servicios
docker-compose exec loans-service ping users-service
```

### **Si hay errores de migración:**
```bash
# Ejecutar migraciones manualmente
docker-compose exec [servicio] python manage.py migrate
```

### **Si Docker Desktop no está ejecutándose:**
1. Abrir Docker Desktop
2. Esperar a que esté completamente iniciado (ícono verde)
3. Ejecutar los comandos nuevamente

---

## 📊 Estado del Sistema

### **Servicios Ejecutándose:**
- ✅ **Usuarios**: `http://localhost:8001` (Página de inicio + API + Admin)
- ✅ **Libros**: `http://localhost:8002` (Página de inicio + API + Admin)
- ✅ **Préstamos**: `http://localhost:8003` (Página de inicio + API + Admin + Arquitectura Hexagonal)

### **🔐 Acceso Rápido al Admin:**
- **Usuario**: `biblioteca_admin` | **Contraseña**: `admin123`
- **URLs**: `http://localhost:8001/admin/` | `http://localhost:8002/admin/` | `http://localhost:8003/admin/`

### **Bases de Datos:**
- ✅ **users_db**: PostgreSQL en puerto 5432
- ✅ **books_db**: PostgreSQL en puerto 5433
- ✅ **loans_db**: PostgreSQL en puerto 5434

### **Funcionalidades Probadas:**
- ✅ Creación de préstamos
- ✅ Límite de préstamos (máximo 3)
- ✅ Usuarios suspendidos
- ✅ Libros eliminados
- ✅ Devolución de préstamos
- ✅ Comunicación entre microservicios
- ✅ Arquitectura hexagonal funcionando

---

## 🎉 ¡Sistema Completamente Funcional!

El **Sistema de Gestión de Biblioteca Digital** está completamente implementado y probado con:

- **3 microservicios** independientes
- **Arquitectura hexagonal** en el microservicio de préstamos
- **Todas las reglas de negocio** implementadas y funcionando
- **Comunicación HTTP/REST** entre servicios
- **Docker** para contenedorización
- **PostgreSQL** para persistencia
- **Documentación completa** y ejemplos de uso

**¡Listo para usar en producción!** 🚀

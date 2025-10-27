# 📚 Sistema de Gestión de Biblioteca Digital

## 🎯 EJERCICIO PRÁCTICO: ARQUITECTURA HEXAGONAL Y MICROSERVICIOS

**Título:** Sistema de Gestión de Biblioteca Digital  
**Nivel:** Básico  
**Tecnologías:** Django, Python, Microservicios  

---

## 📋 DESCRIPCIÓN DEL EJERCICIO

### 1. CONTEXTO Y OBJETIVO
Una biblioteca digital necesita modernizar su sistema de préstamos. Debes desarrollar una plataforma distribuida que gestione préstamos de libros digitales aplicando **arquitectura hexagonal** en el componente principal.

### 2. DESCRIPCIÓN DEL SISTEMA
El sistema está compuesto por **3 microservicios independientes**:

- **Microservicio de Préstamos** (desarrollo principal con arquitectura hexagonal)
- **Microservicio de Libros**
- **Microservicio de Usuarios**

### 3. REQUISITOS FUNCIONALES

#### 3.1 Flujo Principal de Préstamos:
1. Usuario solicita préstamo de un libro
2. Validar que el usuario existe y está activo
3. Verificar que el libro existe y está disponible
4. Registrar el préstamo con fechas de inicio y vencimiento
5. Actualizar estado del libro a "prestado"

#### 3.2 Reglas de Negocio:
- ✅ Límite de **3 préstamos activos** por usuario
- ✅ Duración máxima de préstamo: **15 días**
- ✅ Usuarios suspendidos no pueden pedir préstamos
- ✅ Libros eliminados no están disponibles

### 4. REQUISITOS TÉCNICOS

#### 4.1 Microservicio de Préstamos:
- ✅ Implementar con **arquitectura hexagonal** en Django
- ✅ Aislamiento completo del dominio de negocio
- ✅ Definición clara de puertos y adaptadores
- ✅ Independencia de frameworks externos

#### 4.2 Comunicación entre Microservicios:
- ✅ Comunicación **HTTP/REST** entre servicios
- ✅ Base de datos **independiente** por microservicio
- ✅ Manejo apropiado de fallos en comunicación

---

## 🚀 INICIO RÁPIDO

### 1. Iniciar el Sistema Completo
```bash
docker-compose up --build
```

### 2. Verificar que Todo Funciona
```bash
# Verificar API Gateway
curl http://localhost:8080/health

# Verificar servicios individuales
curl http://localhost:8001/health/  # Usuarios
curl http://localhost:8002/health/  # Libros  
curl http://localhost:8003/health/  # Préstamos
```

### 3. Probar el Sistema (Windows)
```powershell
# Ejecutar script de prueba automático
.\test-api-gateway.ps1
```

---

## 🌐 URLs del Sistema

### API Gateway (Punto de Entrada Único)
| Servicio | URL |
|----------|-----|
| **Información** | http://localhost:8080/ |
| **Health Check** | http://localhost:8080/health |
| **Usuarios** | http://localhost:8080/api/users/ |
| **Libros** | http://localhost:8080/api/books/ |
| **Préstamos** | http://localhost:8080/api/loans/ |

### Servicios Individuales
| Servicio | Puerto | URL Base | Admin |
|----------|--------|----------|-------|
| **Usuarios** | 8001 | http://localhost:8001/api/users/ | http://localhost:8001/admin/ |
| **Libros** | 8002 | http://localhost:8002/api/books/ | http://localhost:8002/admin/ |
| **Préstamos** | 8003 | http://localhost:8003/api/loans/ | http://localhost:8003/admin/ |

---

## 🏗️ ARQUITECTURA HEXAGONAL (Microservicio de Préstamos)

### Estructura del Proyecto
```
loan-service/
├── loans/
│   ├── domain/           # 🎯 NÚCLEO DEL DOMINIO
│   │   ├── entities.py   # Entidades de negocio
│   │   ├── ports.py      # Interfaces (contratos)
│   │   └── exceptions.py # Excepciones de dominio
│   ├── application/      # 🔄 CAPA DE APLICACIÓN
│   │   ├── use_cases.py  # Casos de uso
│   │   └── services.py   # Servicios de aplicación
│   └── infrastructure/   # 🔌 CAPA DE INFRAESTRUCTURA
│       ├── repositories.py    # Adaptadores de persistencia
│       ├── services.py        # Adaptadores de servicios externos
│       ├── views.py           # Adaptadores de entrada HTTP
│       └── serializers.py     # Adaptadores de serialización
```

### Principios Aplicados
- ✅ **Inversión de Dependencias**: El dominio no depende de la infraestructura
- ✅ **Puertos y Adaptadores**: Interfaces claras entre capas
- ✅ **Aislamiento del Dominio**: Lógica de negocio independiente de frameworks
- ✅ **Testabilidad**: Cada capa se puede probar independientemente

---

## 📊 ENTREGABLES COMPLETADOS

### ✅ Código Fuente
- **Microservicio de Préstamos** con arquitectura hexagonal completa
- **Microservicio de Libros** funcional
- **Microservicio de Usuarios** funcional
- **API Gateway** para centralizar el acceso

### ✅ Comunicación Demostrada
- HTTP/REST entre los 3 servicios
- Bases de datos PostgreSQL independientes
- Manejo de errores y fallos de comunicación

### ✅ Documentación
- Instrucciones de instalación y uso
- Ejemplos de API
- Scripts de prueba automatizados

---

## 🧪 PRUEBAS DEL SISTEMA

### Crear un Usuario
```bash
curl -X POST http://localhost:8080/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@biblioteca.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "555-1234",
    "address": "Calle Principal 123",
    "membership_number": "MEM001"
  }'
```

### Crear un Libro
```bash
curl -X POST http://localhost:8080/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "El Quijote",
    "author": "Miguel de Cervantes",
    "isbn": "9788420412146",
    "publisher": "Editorial Alfaguara",
    "publication_year": 1605,
    "genre": "Novela",
    "description": "Las aventuras del ingenioso hidalgo"
  }'
```

### Crear un Préstamo
```bash
curl -X POST http://localhost:8080/api/loans/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "book_id": 1
  }'
```

---

## 🛠️ TECNOLOGÍAS UTILIZADAS

- **Backend**: Django + Python 3.11
- **Base de Datos**: PostgreSQL 15
- **Contenedores**: Docker + Docker Compose
- **API**: Django REST Framework
- **Gateway**: Nginx
- **Arquitectura**: Hexagonal (Ports & Adapters)

---

## 📁 ESTRUCTURA FINAL DEL PROYECTO

```
Sistema de Gestión de Biblioteca Digital/
├── api-gateway/              # API Gateway con Nginx
├── user-service/             # Microservicio de Usuarios
├── book-service/             # Microservicio de Libros
├── loan-service/             # Microservicio de Préstamos (Arquitectura Hexagonal)
├── docker-compose.yml        # Orquestación de servicios
├── test-api-gateway.ps1      # Script de prueba automático
├── test-sistema.ps1          # Script de prueba general
├── env-example.txt           # Variables de entorno de ejemplo
└── README.md                 # Este archivo
```

---

## 🎯 OBJETIVOS CUMPLIDOS

✅ **Arquitectura Hexagonal** implementada en el microservicio de préstamos  
✅ **3 microservicios independientes** funcionando  
✅ **Comunicación HTTP/REST** entre servicios  
✅ **Bases de datos independientes** por microservicio  
✅ **API Gateway** centralizando el acceso  
✅ **Reglas de negocio** implementadas correctamente  
✅ **Documentación completa** y scripts de prueba  

---

**🎉 El ejercicio está completamente implementado y funcionando.**  
**Sistema listo para demostrar arquitectura hexagonal y microservicios.** 🚀
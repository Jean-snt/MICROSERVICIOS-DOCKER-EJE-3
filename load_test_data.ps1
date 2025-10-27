# Script de datos de prueba para Windows PowerShell
# Sistema de Biblioteca Digital

Write-Host "=== Cargando datos de prueba para el Sistema de Biblioteca Digital ===" -ForegroundColor Green

# Esperar a que los servicios estén listos
Write-Host "Esperando a que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Crear usuarios de prueba
Write-Host "Creando usuarios de prueba..." -ForegroundColor Cyan

$user1 = @{
    name = "Juan Pérez"
    email = "juan@example.com"
    status = "active"
} | ConvertTo-Json

$user2 = @{
    name = "María García"
    email = "maria@example.com"
    status = "active"
} | ConvertTo-Json

$user3 = @{
    name = "Carlos López"
    email = "carlos@example.com"
    status = "suspended"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://localhost:8001/api/users/" -Method POST -Body $user1 -ContentType "application/json"
    Write-Host "Usuario Juan Pérez creado" -ForegroundColor Green
    
    Invoke-RestMethod -Uri "http://localhost:8001/api/users/" -Method POST -Body $user2 -ContentType "application/json"
    Write-Host "Usuario María García creado" -ForegroundColor Green
    
    Invoke-RestMethod -Uri "http://localhost:8001/api/users/" -Method POST -Body $user3 -ContentType "application/json"
    Write-Host "Usuario Carlos López creado" -ForegroundColor Green
} catch {
    Write-Host "Error creando usuarios: $($_.Exception.Message)" -ForegroundColor Red
}

# Crear libros de prueba
Write-Host "Creando libros de prueba..." -ForegroundColor Cyan

$book1 = @{
    title = "Python para Principiantes"
    author = "Autor Python"
    isbn = "1234567890123"
    description = "Libro introductorio de Python"
} | ConvertTo-Json

$book2 = @{
    title = "Django Avanzado"
    author = "Autor Django"
    isbn = "1234567890124"
    description = "Guía avanzada de Django"
} | ConvertTo-Json

$book3 = @{
    title = "Arquitectura de Software"
    author = "Autor Arquitectura"
    isbn = "1234567890125"
    description = "Patrones y arquitecturas de software"
} | ConvertTo-Json

$book4 = @{
    title = "Microservicios"
    author = "Autor Microservicios"
    isbn = "1234567890126"
    description = "Diseño de microservicios"
} | ConvertTo-Json

$book5 = @{
    title = "Libro Eliminado"
    author = "Autor Eliminado"
    isbn = "1234567890127"
    description = "Este libro será eliminado"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://localhost:8002/api/books/" -Method POST -Body $book1 -ContentType "application/json"
    Write-Host "Libro Python para Principiantes creado" -ForegroundColor Green
    
    Invoke-RestMethod -Uri "http://localhost:8002/api/books/" -Method POST -Body $book2 -ContentType "application/json"
    Write-Host "Libro Django Avanzado creado" -ForegroundColor Green
    
    Invoke-RestMethod -Uri "http://localhost:8002/api/books/" -Method POST -Body $book3 -ContentType "application/json"
    Write-Host "Libro Arquitectura de Software creado" -ForegroundColor Green
    
    Invoke-RestMethod -Uri "http://localhost:8002/api/books/" -Method POST -Body $book4 -ContentType "application/json"
    Write-Host "Libro Microservicios creado" -ForegroundColor Green
    
    Invoke-RestMethod -Uri "http://localhost:8002/api/books/" -Method POST -Body $book5 -ContentType "application/json"
    Write-Host "Libro Libro Eliminado creado" -ForegroundColor Green
} catch {
    Write-Host "Error creando libros: $($_.Exception.Message)" -ForegroundColor Red
}

# Eliminar el último libro para probar la funcionalidad
Write-Host "Eliminando libro de prueba..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "http://localhost:8002/api/books/5/delete_book/" -Method POST
    Write-Host "Libro eliminado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "Error eliminando libro: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Datos de prueba cargados exitosamente ===" -ForegroundColor Green
Write-Host ""
Write-Host "Usuarios creados:" -ForegroundColor Yellow
Write-Host "- Juan Pérez (ID: 1) - Activo"
Write-Host "- María García (ID: 2) - Activo" 
Write-Host "- Carlos López (ID: 3) - Suspendido"
Write-Host ""
Write-Host "Libros creados:" -ForegroundColor Yellow
Write-Host "- Python para Principiantes (ID: 1) - Disponible"
Write-Host "- Django Avanzado (ID: 2) - Disponible"
Write-Host "- Arquitectura de Software (ID: 3) - Disponible"
Write-Host "- Microservicios (ID: 4) - Disponible"
Write-Host "- Libro Eliminado (ID: 5) - Eliminado"
Write-Host ""
Write-Host "Puedes probar el sistema con los siguientes comandos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "# Verificar si Juan puede pedir préstamo:" -ForegroundColor White
Write-Host "Invoke-RestMethod -Uri 'http://localhost:8003/api/loans/check_user_can_borrow/?user_id=1'" -ForegroundColor Gray
Write-Host ""
Write-Host "# Crear un préstamo:" -ForegroundColor White
Write-Host '$loan = @{user_id = 1; book_id = 1} | ConvertTo-Json' -ForegroundColor Gray
Write-Host "Invoke-RestMethod -Uri 'http://localhost:8003/api/loans/' -Method POST -Body `$loan -ContentType 'application/json'" -ForegroundColor Gray
Write-Host ""
Write-Host "# Ver préstamos activos de Juan:" -ForegroundColor White
Write-Host "Invoke-RestMethod -Uri 'http://localhost:8003/api/loans/user_active_loans/?user_id=1'" -ForegroundColor Gray
Write-Host ""
Write-Host "# Intentar préstamo con usuario suspendido (debería fallar):" -ForegroundColor White
Write-Host '$loan = @{user_id = 3; book_id = 2} | ConvertTo-Json' -ForegroundColor Gray
Write-Host "Invoke-RestMethod -Uri 'http://localhost:8003/api/loans/' -Method POST -Body `$loan -ContentType 'application/json'" -ForegroundColor Gray

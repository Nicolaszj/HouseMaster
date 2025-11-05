@echo off
echo ====================================
echo   HouseMaster - Docker Deployment
echo ====================================
echo.

echo [1/5] Construyendo imagenes Docker...
docker-compose build
if %errorlevel% neq 0 (
    echo ERROR: Fallo al construir imagenes
    pause
    exit /b 1
)

echo.
echo [2/5] Levantando servicios...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Fallo al levantar servicios
    pause
    exit /b 1
)

echo.
echo [3/5] Esperando a que MySQL este listo...
timeout /t 20 /nobreak

echo.
echo [4/5] Ejecutando migraciones...
docker-compose exec web python manage.py migrate
if %errorlevel% neq 0 (
    echo ADVERTENCIA: Algunas migraciones fallaron
)

echo.
echo [5/5] Recolectando archivos estaticos...
docker-compose exec web python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ADVERTENCIA: Fallo al recolectar estaticos
)

echo.
echo ====================================
echo   Despliegue Completado!
echo ====================================
echo.
echo Aplicacion: http://localhost:8000
echo Admin: http://localhost:8000/admin
echo API Docs: http://localhost:8000/api/docs/
echo.
echo Comandos utiles:
echo   Ver logs: docker-compose logs -f
echo   Detener: docker-compose down
echo   Reiniciar: docker-compose restart web
echo.
pause

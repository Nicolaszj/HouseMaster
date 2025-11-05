@echo off
echo ========================================
echo  Instalador de Gettext para Windows
echo ========================================
echo.
echo Este script instalara gettext necesario para las traducciones.
echo.

REM Verificar si gettext ya esta instalado
where msgfmt >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Gettext ya esta instalado!
    msgfmt --version
    echo.
    echo Ahora puedes compilar las traducciones:
    echo   python manage.py compilemessages
    pause
    exit /b 0
)

echo [!] Gettext NO esta instalado
echo.
echo Opciones de instalacion:
echo.
echo 1. CHOCOLATEY (Recomendado - requiere chocolatey instalado)
echo    choco install gettext
echo.
echo 2. DESCARGA MANUAL
echo    https://github.com/mlocati/gettext-iconv-windows/releases
echo    Descarga: gettext0.21-iconv1.16-static-64.exe
echo.
echo 3. SCOOP (si tienes Scoop instalado)
echo    scoop install gettext
echo.
echo ========================================
echo.

REM Intentar instalar con chocolatey
where choco >nul 2>nul
if %errorlevel% equ 0 (
    echo Se detecto Chocolatey instalado.
    echo.
    set /p instalar="Deseas instalar gettext con Chocolatey? (S/N): "
    if /i "%instalar%"=="S" (
        echo.
        echo Instalando gettext con Chocolatey...
        choco install gettext -y
        
        if %errorlevel% equ 0 (
            echo.
            echo [OK] Gettext instalado correctamente!
            echo.
            echo Ahora ejecuta:
            echo   python manage.py compilemessages
            echo   python manage.py runserver
            pause
            exit /b 0
        ) else (
            echo.
            echo [ERROR] Fallo la instalacion
            pause
            exit /b 1
        )
    )
)

echo.
echo Por favor instala gettext manualmente:
echo 1. Ve a: https://github.com/mlocati/gettext-iconv-windows/releases
echo 2. Descarga: gettext0.21-iconv1.16-static-64.exe
echo 3. Ejecuta el instalador
echo 4. Agrega la carpeta bin a tu PATH
echo 5. Reinicia tu terminal
echo.
pause

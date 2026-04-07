@echo off
echo ================================================
echo  INSTALADOR CLOUDFLARE TUNNEL - Windows
echo ================================================
echo.
echo Este script descarga e instala cloudflared.exe
echo.
pause

echo.
echo [1/3] Descargando cloudflared.exe...
echo.

:: URL de descarga desde artifacts.walmart.com (espejo de GitHub)
set DOWNLOAD_URL=https://generic.ci.artifacts.walmart.com/artifactory/github-releases-generic-release-remote/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe

echo Descargando desde: %DOWNLOAD_URL%
echo.

:: Usar curl para descargar (Windows 10+ lo tiene por defecto)
curl -L -o cloudflared.exe "%DOWNLOAD_URL%" --proxy http://sysproxy.wal-mart.com:8080 --insecure

if not exist cloudflared.exe (
    echo.
    echo ERROR: No se pudo descargar cloudflared.exe
    echo.
    echo Intenta descargarlo manualmente:
    echo 1. Ve a: https://github.com/cloudflare/cloudflared/releases
    echo 2. Descarga: cloudflared-windows-amd64.exe
    echo 3. Renombralo a: cloudflared.exe
    echo 4. Ponlo en esta carpeta: %CD%
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Verificando instalacion...
cloudflared.exe --version

if errorlevel 1 (
    echo.
    echo ERROR: cloudflared.exe no funciona correctamente
    pause
    exit /b 1
)

echo.
echo [3/3] Instalacion completada!
echo.
echo Archivo instalado en: %CD%\cloudflared.exe
echo.
echo ================================================
echo  PROXIMO PASO: Crear tunel
echo ================================================
echo.
echo 1. Abre una NUEVA terminal
echo 2. Ve a esta carpeta: cd %CD%
echo 3. Ejecuta: cloudflared.exe tunnel --url http://localhost:8002
echo.
echo Eso te dara una URL publica tipo: https://xyz.trycloudflare.com
echo.
pause

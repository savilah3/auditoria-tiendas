@echo off
echo ================================================
echo  INSTALADOR CLOUDFLARE TUNNEL - Mejorado
echo ================================================
echo.
echo Detectando proxies de Walmart...
echo.

:: Intentar multiples metodos de descarga

echo [Intento 1/4] Descarga directa desde GitHub (sin proxy)...
curl -L -o cloudflared.exe "https://github.com/cloudflare/cloudflared/releases/download/2024.12.2/cloudflared-windows-amd64.exe" --ssl-no-revoke --insecure 2>nul

if exist cloudflared.exe (
    echo.
    echo [SUCCESS] Descarga exitosa!
    goto :verify
)

echo [FALLO] Reintentando...
echo.

echo [Intento 2/4] Descarga CON proxy Walmart...
curl -L -o cloudflared.exe "https://github.com/cloudflare/cloudflared/releases/download/2024.12.2/cloudflared-windows-amd64.exe" --proxy http://sysproxy.wal-mart.com:8080 --ssl-no-revoke --insecure 2>nul

if exist cloudflared.exe (
    echo.
    echo [SUCCESS] Descarga exitosa con proxy!
    goto :verify
)

echo [FALLO] Reintentando...
echo.

echo [Intento 3/4] Usando artifacts.walmart.com...
curl -L -o cloudflared.exe "https://generic.ci.artifacts.walmart.com/artifactory/github-releases-generic-release-remote/cloudflare/cloudflared/releases/download/2024.12.2/cloudflared-windows-amd64.exe" --proxy http://sysproxy.wal-mart.com:8080 --ssl-no-revoke --insecure 2>nul

if exist cloudflared.exe (
    echo.
    echo [SUCCESS] Descarga exitosa desde artifacts!
    goto :verify
)

echo [FALLO] Reintentando...
echo.

echo [Intento 4/4] PowerShell Download...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $webClient = New-Object System.Net.WebClient; $webClient.Proxy = New-Object System.Net.WebProxy('http://sysproxy.wal-mart.com:8080'); $webClient.DownloadFile('https://github.com/cloudflare/cloudflared/releases/download/2024.12.2/cloudflared-windows-amd64.exe', 'cloudflared.exe')}" 2>nul

if exist cloudflared.exe (
    echo.
    echo [SUCCESS] Descarga exitosa con PowerShell!
    goto :verify
)

echo.
echo ================================================
echo  ERROR: Todos los metodos de descarga fallaron
echo ================================================
echo.
echo SOLUCION: Descarga MANUAL
echo.
echo 1. Abre en tu navegador:
echo    https://github.com/cloudflare/cloudflared/releases/latest
echo.
echo 2. Busca y descarga: cloudflared-windows-amd64.exe
echo.
echo 3. Renombralo a: cloudflared.exe
echo.
echo 4. Muevelo a: %CD%
echo.
pause
exit /b 1

:verify
echo.
echo Verificando instalacion...
cloudflared.exe --version

if errorlevel 1 (
    echo.
    echo ERROR: El archivo descargado no funciona
    del cloudflared.exe
    echo Intenta descarga manual.
    pause
    exit /b 1
)

echo.
echo ================================================
echo  INSTALACION EXITOSA!
echo ================================================
echo.
echo Archivo instalado: %CD%\cloudflared.exe
echo.
cloudflared.exe --version
echo.
echo Ahora puedes ejecutar: CREAR_TUNEL.bat
echo.
pause

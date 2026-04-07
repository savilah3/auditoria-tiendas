@echo off
echo ================================================
echo  INSTALADOR NGROK - Alternativa a Cloudflare
echo ================================================
echo.
echo Ngrok funciona MEJOR en redes corporativas Walmart
echo.
pause

echo.
echo [1/2] Descargando ngrok...
echo.

curl -L -o ngrok.zip "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip" --proxy http://sysproxy.wal-mart.com:8080 --ssl-no-revoke --insecure

if not exist ngrok.zip (
    echo.
    echo ERROR: Descarga fallo
    echo.
    echo Descarga manual:
    echo 1. Ve a: https://ngrok.com/download
    echo 2. Descarga version Windows (64-bit)
    echo 3. Descomprime ngrok.exe aqui: %CD%
    echo.
    pause
    exit /b 1
)

echo.
echo [2/2] Descomprimiendo...
powershell -Command "Expand-Archive -Path ngrok.zip -DestinationPath . -Force"

if exist ngrok.exe (
    echo.
    echo [SUCCESS] ngrok instalado correctamente!
    del ngrok.zip
    echo.
    echo Archivo: %CD%\ngrok.exe
    echo.
) else (
    echo.
    echo ERROR: Descompresion fallo
    echo Descomprime ngrok.zip manualmente
    pause
    exit /b 1
)

echo.
echo ================================================
echo  INSTALACION EXITOSA!
echo ================================================
echo.
echo Ahora ejecuta: CREAR_TUNEL_NGROK.bat
echo.
pause

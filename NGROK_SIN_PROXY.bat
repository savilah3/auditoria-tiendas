@echo off
echo ================================================
echo  NGROK TUNNEL - Intento SIN PROXY
echo ================================================
echo.
echo Intentando conectar ngrok SIN pasar por proxy...
echo (A veces funciona en redes corporativas)
echo.
pause

if not exist ngrok.exe (
    echo ERROR: ngrok.exe no encontrado
    pause
    exit /b 1
)

echo.
echo [+] Creando tunel...
echo.

:: Limpiar variables de proxy
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=

ngrok.exe http 8002 --log=stdout

pause

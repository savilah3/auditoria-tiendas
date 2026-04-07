@echo off
echo ================================================
echo  NGROK TUNNEL - Auditoría Tiendas
echo ================================================
echo.
echo ANTES DE CONTINUAR:
echo 1. Servidor LOCAL debe estar corriendo (INICIAR_LOCAL.bat)
echo 2. ngrok.exe debe estar instalado (INSTALAR_NGROK.bat)
echo.
pause

if not exist ngrok.exe (
    echo.
    echo ERROR: ngrok.exe no encontrado
    echo.
    echo Ejecuta primero: INSTALAR_NGROK.bat
    echo.
    pause
    exit /b 1
)

echo.
echo [+] Creando tunel publico con ngrok...
echo [+] Puerto local: 8002
echo.
echo TU URL PUBLICA aparecera abajo (busca "Forwarding")
echo Ejemplo: https://abc123.ngrok-free.app
echo ================================================================
echo.

:: Configurar proxy para ngrok
set HTTP_PROXY=http://sysproxy.wal-mart.com:8080
set HTTPS_PROXY=http://sysproxy.wal-mart.com:8080

ngrok.exe http 8002

pause

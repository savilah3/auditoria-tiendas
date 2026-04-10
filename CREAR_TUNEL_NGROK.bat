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
echo [+] Configurando proxy Walmart...
echo.
echo TU URL PUBLICA aparecera abajo (busca "Forwarding")
echo Ejemplo: https://abc123.ngrok-free.app
echo ================================================================
echo.

:: Usar archivo de configuración con proxy
ngrok.exe http 8002 --config=ngrok.yml --log=stdout

pause

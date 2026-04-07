@echo off
echo ================================================
echo  CLOUDFLARE TUNNEL - Auditoría Tiendas
echo ================================================
echo.
echo IMPORTANTE: Antes de ejecutar esto, asegurate de que:
echo 1. El servidor LOCAL este corriendo (INICIAR_LOCAL.bat)
echo 2. cloudflared.exe este instalado (INSTALAR_CLOUDFLARE.bat)
echo.
pause

if not exist cloudflared.exe (
    echo.
    echo ERROR: cloudflared.exe no encontrado
    echo.
    echo Ejecuta primero: INSTALAR_CLOUDFLARE.bat
    echo.
    pause
    exit /b 1
)

echo.
echo [+] Creando tunel publico...
echo [+] Puerto local: 8002
echo.
echo TU URL PUBLICA aparecera abajo (busca "trycloudflare.com")
echo ================================================================
echo.

cloudflared.exe tunnel --url http://localhost:8002

pause

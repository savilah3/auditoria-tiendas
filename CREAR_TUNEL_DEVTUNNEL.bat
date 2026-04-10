@echo off
echo ================================================
echo  VISUAL STUDIO DEV TUNNELS - Alternativa
echo ================================================
echo.
echo VS Dev Tunnels funciona MEJOR en redes Walmart
echo (Usa autenticacion Microsoft integrada)
echo.
pause

echo.
echo [1/3] Verificando si 'devtunnel' esta instalado...

:: Buscar devtunnel en varias ubicaciones
set DEVTUNNEL_PATH="%LOCALAPPDATA%\Microsoft\WinGet\Links\devtunnel.exe"
if not exist %DEVTUNNEL_PATH% (
    where devtunnel >nul 2>&1
    if errorlevel 1 (
        echo.
        echo [ERROR] 'devtunnel' no encontrado.
        echo.
        echo INSTALACION:
        echo    winget install Microsoft.devtunnel
        echo.
        echo Luego REINICIA ESTA TERMINAL y vuelve a ejecutar.
        echo.
        pause
        exit /b 1
    ) else (
        set DEVTUNNEL_PATH=devtunnel
    )
)

echo [OK] devtunnel encontrado
echo.

echo [2/3] Creando tunel (requiere login Microsoft)...
echo.
echo IMPORTANTE:
echo - Te pedira login con tu cuenta Microsoft/Walmart
echo - Acepta los permisos
echo - El tunel se creara automaticamente
echo.
pause

echo.
echo Iniciando tunel...
echo.

%DEVTUNNEL_PATH% host -p 8002 --allow-anonymous

echo.
echo ================================================
echo  TUNEL FINALIZADO
echo ================================================
echo.
echo Si viste "Ready to accept connections for tunnel"
echo significa que funciono!
echo.
echo La URL estaba arriba en formato:
echo "Connect via browser: https://xxxxx.devtunnels.ms"
echo.
pause

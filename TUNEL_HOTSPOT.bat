@echo off
echo ================================================
echo  COMPARTIR VIA HOTSPOT + NGROK
echo ================================================
echo.
echo ESTA ES LA SOLUCION MAS RAPIDA!
echo.
echo PASOS:
echo.
echo 1. Desconecta tu PC del WiFi Walmart
echo 2. Activa el HOTSPOT de tu celular (datos moviles)
echo 3. Conecta tu PC a tu hotspot
echo 4. Ejecuta este script nuevamente
echo.
echo Al usar datos moviles (no WiFi Walmart):
echo - ngrok funcionara sin bloqueos
echo - Obtendras URL publica
echo - Podras compartir con quien quieras
echo.
pause

echo.
echo Verificando conexion...
ping -n 1 google.com >nul 2>&1
if errorlevel 1 (
    echo ERROR: No hay conexion a internet
    echo Conectate al hotspot de tu celular primero
    pause
    exit /b 1
)

echo OK - Conexion detectada
echo.
echo Creando tunel ngrok con datos moviles...
echo.

ngrok.exe http 8002 --log=stdout

pause

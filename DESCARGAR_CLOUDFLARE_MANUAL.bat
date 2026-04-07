@echo off
echo ================================================
echo  DESCARGA MANUAL - Cloudflare Tunnel
echo ================================================
echo.
echo El script automatico fallo. Descarga manualmente:
echo.
echo PASO 1: Abre esta URL en tu navegador:
echo.
echo https://github.com/cloudflare/cloudflared/releases/latest
echo.
echo PASO 2: Busca el archivo que diga:
echo.
echo    cloudflared-windows-amd64.exe
echo.
echo PASO 3: Descargalo
echo.
echo PASO 4: Renombralo a:  cloudflared.exe
echo.
echo PASO 5: Muevelo a esta carpeta:
echo    %CD%
echo.
echo PASO 6: Vuelve a ejecutar: CREAR_TUNEL.bat
echo.
echo ================================================
echo.
echo ALTERNATIVA: Copiare la URL directa al portapapeles
echo.
pause

:: URL directa del release más reciente (actualizada)
set DOWNLOAD_URL=https://github.com/cloudflare/cloudflared/releases/download/2024.12.2/cloudflared-windows-amd64.exe

echo.
echo Intentando abrir GitHub releases...
start "" "%DOWNLOAD_URL%"

echo.
echo Si no abre, copia esta URL manualmente:
echo %DOWNLOAD_URL%
echo.
pause

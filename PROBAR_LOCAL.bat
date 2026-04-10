@echo off
echo ========================================
echo PRUEBA LOCAL - VISITAS CON SENTIDO V2
echo ========================================
echo.
echo Este script inicia el servidor localmente para probar los cambios
echo ANTES de hacer deploy a Render.
echo.
echo Requisitos:
echo  - Python instalado
echo  - DATABASE_URL configurado en .env (o usar SQLite local)
echo.
pause

cd /d "%~dp0"

echo.
echo [1/4] Verificando archivos actualizados...
if not exist "templates\visitas.html" (
    echo ERROR: templates\visitas.html no encontrado
    pause
    exit /b 1
)
echo OK: templates\visitas.html existe

if not exist "database.py" (
    echo ERROR: database.py no encontrado
    pause
    exit /b 1
)
echo OK: database.py existe

if not exist "main.py" (
    echo ERROR: main.py no encontrado
    pause
    exit /b 1
)
echo OK: main.py existe

echo.
echo [2/4] Verificando dependencias...
python -c "import fastapi, uvicorn, psycopg" 2>nul
if errorlevel 1 (
    echo.
    echo Instalando dependencias...
    pip install -r requirements.txt --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com
)
echo OK: Dependencias instaladas

echo.
echo [3/4] Iniciando servidor local...
echo.
echo El servidor estara disponible en: http://localhost:8000/visitas
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
timeout /t 3

python -m uvicorn main:app --reload --port 8000

pause

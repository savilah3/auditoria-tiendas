@echo off
echo ========================================
echo COMMIT Y PUSH A GIT - VISITAS V2
echo ========================================
echo.
echo Este script hace commit de todos los cambios y los pushea al repositorio.
echo.
echo Archivos que se commitearán:
echo  - templates/visitas.html (nuevo formulario)
echo  - database.py (nuevos campos + migración)
echo  - main.py (endpoint actualizado)
echo  - RESUMEN_ACTUALIZACION_V2.txt (documentación)
echo.
pause

cd /d "%~dp0"

echo.
echo [1/3] Verificando estado de git...
git status

echo.
echo [2/3] Agregando archivos...
git add templates/visitas.html
git add database.py
git add main.py
git add RESUMEN_ACTUALIZACION_V2.txt
git add MIGRACION_NUEVOS_CAMPOS.sql

echo.
echo [3/3] Haciendo commit...
git commit -m "feat: Actualizar formulario Visitas con Sentido v2

- Nuevos campos de atención: q3-q7, q8_csat, q9_new
- Función enviarFormulario() con loading 'Enviando...'
- Geolocalización automática
- Migración automática de BD para preservar datos existentes
- Actualizado export Excel con nuevas columnas

Cambios principales:
- templates/visitas.html: Nuevo formulario con mejoras de UX
- database.py: Nuevos campos + migración automática
- main.py: Endpoint /submit-visita actualizado
"

echo.
echo Commit realizado exitosamente!
echo.
set /p PUSH="Deseas hacer PUSH al repositorio remoto? (S/N): "
if /i "%PUSH%"=="S" (
    echo.
    echo Haciendo push...
    git push origin main
    echo.
    echo PUSH completado!
    echo.
    echo El deploy automatico en Render deberia iniciar en unos segundos.
    echo Revisa: https://dashboard.render.com
) else (
    echo.
    echo Push cancelado. Puedes hacerlo manualmente mas tarde con:
    echo git push origin main
)

echo.
pause

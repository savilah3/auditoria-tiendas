@echo off
echo ====================================
echo  AUDITORIA TIENDAS - LOCAL SERVER
echo ====================================
echo.
echo [1/2] Activando entorno virtual...
call .venv\Scripts\activate
echo [2/2] Iniciando servidor local...
echo Puerto: 8002
echo Database: auditoria_local.db (SQLite)
echo.
echo Accede a: http://localhost:8002
echo.

python main_local.py

pause

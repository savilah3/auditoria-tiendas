"""
Script de migración para:
1. Cambiar Q9 a "Cartelería TyC"
2. Agregar columna tiempo_fila
3. Verificar estructura completa
"""
import sys
sys.path.insert(0, 'C:\\Users\\savila3\\Documents\\puppy_workspace\\auditoria_tiendas')

print("=" * 70)
print("MIGRACIÓN: Q9 → Cartelería TyC + Timer")
print("=" * 70)

# Mostrar cambios necesarios
print("\n✅ CAMBIOS A REALIZAR:\n")

print("1️⃣ BASE DE DATOS:")
print("   - Cambiar nombre columna: q9_new → q9_carteleria (o mantener q9_new)")
print("   - Agregar columna: tiempo_fila TEXT")
print()

print("2️⃣ FORMULARIO (visitas.html):")
print("   - Cambiar texto Q9:")
print("     ANTES: '9. ¿Te sentiste bienvenido durante tu visita?'")
print("     AHORA: '9. ¿La cartelería de Términos y Condiciones está visible?'")
print()

print("3️⃣ DASHBOARD (dashboard.html):")
print("   - Cambiar header columna Q9:")
print("     ANTES: 'Q9<br>Bienvenida'")
print("     AHORA: 'Q9<br>Cartelería TyC'")
print("   - Agregar columna Timer")
print()

print("4️⃣ ENDPOINT (main.py):")
print("   - Agregar parámetro: tiempo_fila: Annotated[str, Form()] = ''")
print("   - Guardar en BD: 'tiempo_fila': tiempo_fila")
print()

print("5️⃣ EXCEL (main.py - exportar_excel):")
print("   - Header: 'Tiempo Fila'")
print("   - Datos: row['tiempo_fila']")
print()

print("6️⃣ ENTREVISTAS:")
print("   - Agregar name= a textareas dinámicos")
print("   - Capturar en endpoint")
print("   - Guardar en tabla entrevistas_visitas")
print("   - Exportar a Excel hoja 2")
print()

print("=" * 70)
print("ESTOS CAMBIOS DEBEN HACERSE MANUALMENTE")
print("=" * 70)

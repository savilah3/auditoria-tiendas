"""
Script de prueba para insertar una visita y verificar que todo funcione
"""
import sys
sys.path.insert(0, 'C:\\Users\\savila3\\Documents\\puppy_workspace\\auditoria_tiendas')

from database import insertar_visita, obtener_todas_visitas, obtener_stats

print("=" * 60)
print("PRUEBA: Insertar visita completa")
print("=" * 60)

# Datos de prueba completos
datos_prueba = {
    "geo_lat": "-33.4569",
    "geo_lng": "-70.6483",
    "usuario": "A0D0N2E",
    "local": "Lider Express Portal La Dehesa",
    # Q3-Q9: Atención
    "q3": "si",
    "q3_otro_text": "",
    "q4": "si",
    "q4_otro_text": "",
    "q5": "si",
    "q5_otro_text": "",
    "q6": "no",
    "q6_otro_text": "",
    "q7": "si",
    "q7_otro_text": "",
    "q8_csat": "7",
    "q9_new": "si",
    "q9_new_otro_text": "",
    # Q8-Q13: Zona de pago
    "q8": "interno",
    "q9": "si",
    "q10": "si",
    "q11": "no",
    "q12": "si",
    "q13": "si",
    # Comentarios
    "q17": "Excelente atención en general. Todo muy limpio y ordenado."
}

print("\n[1] Insertando visita de prueba...")
try:
    visita_id = insertar_visita(datos_prueba)
    print(f"✅ Visita insertada con ID: {visita_id}")
except Exception as e:
    print(f"❌ Error al insertar: {e}")
    sys.exit(1)

print("\n[2] Obteniendo todas las visitas...")
try:
    visitas = obtener_todas_visitas()
    print(f"✅ Total de visitas en BD: {len(visitas)}")
    if visitas:
        print(f"✅ Primera visita: {visitas[0]['id']} - {visitas[0]['local']}")
except Exception as e:
    print(f"❌ Error al obtener visitas: {e}")

print("\n[3] Obteniendo stats...")
try:
    stats = obtener_stats()
    print(f"✅ Stats:")
    print(f"   - Punto de Compra: {stats['total_punto_compra']}")
    print(f"   - Visitas: {stats['total_visitas']}")
except Exception as e:
    print(f"❌ Error al obtener stats: {e}")

print("\n[4] Verificando campos guardados...")
if visitas:
    v = visitas[0]
    print(f"   - Usuario: {v.get('usuario', 'N/A')}")
    print(f"   - Local: {v.get('local', 'N/A')}")
    print(f"   - Q3 (Guardia saludó): {v.get('q3', 'N/A')}")
    print(f"   - Q8_CSAT: {v.get('q8_csat', 'N/A')}")
    print(f"   - Q9_new (Bienvenida): {v.get('q9_new', 'N/A')}")
    print(f"   - Q8 (Tipo cajero): {v.get('q8', 'N/A')}")
    print(f"   - Q9 (Cajero saludó): {v.get('q9', 'N/A')}")
    print(f"   - Q17 (Comentarios): {v.get('q17', 'N/A')[:50]}...")

print("\n" + "=" * 60)
print("✅ PRUEBA COMPLETADA")
print("=" * 60)

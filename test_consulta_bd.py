"""
Script para consultar BD y ver qué campos se guardaron
"""
import sys
sys.path.insert(0, 'C:\\Users\\savila3\\Documents\\puppy_workspace\\auditoria_tiendas')

from database import get_conn

print("=" * 70)
print("CONSULTANDO ÚLTIMA VISITA EN BD")
print("=" * 70)

with get_conn() as conn:
    # Ver qué columnas tiene la tabla
    columnas = conn.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'visitas'
        ORDER BY ordinal_position
    """).fetchall()
    
    print(f"\n✅ COLUMNAS EN TABLA VISITAS ({len(columnas)} total):\n")
    for i, col in enumerate(columnas, 1):
        print(f"   {i:2d}. {col['column_name']}")
    
    # Obtener última visita
    visita = conn.execute("""
        SELECT * FROM visitas ORDER BY id DESC LIMIT 1
    """).fetchone()
    
    if visita:
        print(f"\n📊 ÚLTIMA VISITA (ID {visita['id']}):\n")
        print(f"   📅 Fecha: {visita.get('fecha', 'N/A')}")
        print(f"   👤 Usuario: {visita.get('usuario', 'N/A')}")
        print(f"   🏪 Local: {visita.get('local', 'N/A')}")
        print(f"   ⏱ Tiempo Fila: {visita.get('tiempo_fila', 'N/A')}")
        
        print(f"\n   📝 CAMPOS DE ATENCIÓN:")
        print(f"      Q3 Guardia saludó: {visita.get('q3', 'N/A')}")
        print(f"      Q3 Otro texto: '{visita.get('q3_otro_text', '')}' {'✅' if visita.get('q3_otro_text') else '❌ vacío'}")
        print(f"      Q4 Guardia preguntó: {visita.get('q4', 'N/A')}")
        print(f"      Q4 Otro texto: '{visita.get('q4_otro_text', '')}' {'✅' if visita.get('q4_otro_text') else '❌ vacío'}")
        print(f"      Q5 Pasillos saludo: {visita.get('q5', 'N/A')}")
        print(f"      Q5 Otro texto: '{visita.get('q5_otro_text', '')}' {'✅' if visita.get('q5_otro_text') else '❌ vacío'}")
        print(f"      Q6 Pasillos preguntaron: {visita.get('q6', 'N/A')}")
        print(f"      Q6 Otro texto: '{visita.get('q6_otro_text', '')}' {'✅' if visita.get('q6_otro_text') else '❌ vacío'}")
        print(f"      Q7 Encontró colaborador: {visita.get('q7', 'N/A')}")
        print(f"      Q7 Otro texto: '{visita.get('q7_otro_text', '')}' {'✅' if visita.get('q7_otro_text') else '❌ vacío'}")
        print(f"      Q8 CSAT: {visita.get('q8_csat', 'N/A')}")
        print(f"      Q9 Cartelería: {visita.get('q9_carteleria', 'N/A')}")
        print(f"      Q9 Cartelería Otro: '{visita.get('q9_carteleria_otro_text', '')}' {'✅' if visita.get('q9_carteleria_otro_text') else '❌ vacío'}")
        
        print(f"\n   💳 CAMPOS ZONA DE PAGO:")
        print(f"      Q8 Tipo cajero: {visita.get('q8', 'N/A')}")
        print(f"      Q9 Cajero saludó: {visita.get('q9', 'N/A')}")
        print(f"      Q10 PMC: {visita.get('q10', 'N/A')}")
        print(f"      Q11 Líder BCI: {visita.get('q11', 'N/A')}")
        print(f"      Q12 Boleta Mail: {visita.get('q12', 'N/A')}")
        print(f"      Q13 Despedida: {visita.get('q13', 'N/A')}")
        
        print(f"\n   💬 COMENTARIOS:")
        print(f"      Q17: '{visita.get('q17', '')}' {'✅' if visita.get('q17') else '❌ vacío'}")
        
        print(f"\n   📍 GEO:")
        print(f"      Lat: {visita.get('geo_lat', 'N/A')}")
        print(f"      Lng: {visita.get('geo_lng', 'N/A')}")
    else:
        print("\n⚠️ NO HAY VISITAS EN LA BD")
        print("   → Resetea la BD y llena el formulario primero")

print("\n" + "=" * 70)
print("CONSULTA COMPLETADA")
print("=" * 70)

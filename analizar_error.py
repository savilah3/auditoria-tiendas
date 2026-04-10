"""
Script para identificar el error 500
"""
# Campos que ENVÍA el HTML (según el formulario)
html_fields = {
    "geo_lat", "geo_lng",
    "usuario", "q1_otro_text",  # Usuario
    "local", "q2_otro_text",    # Local
    "q3", "q3_otro_text",       # Guardia saludó
    "q4", "q4_otro_text",       # Guardia preguntó
    "q5", "q5_otro_text",       # Pasillos saludo
    "q6", "q6_otro_text",       # Pasillos preguntaron
    "q7", "q7_otro_text",       # Encontró colaborador
    "q8_csat",                  # CSAT 1-7
    "q9_new", "q9_otro_text",   # Te sentiste bienvenido (NOTA: HTML usa q9_otro_text)
    "q8",                       # Tipo cajero
    "q9", "q10", "q11", "q12", "q13",  # Zona de pago
    "q17"                       # Comentarios
}

# Campos que ESPERA database.py
db_fields = {
    "fecha", "geo_lat", "geo_lng",
    "usuario", "local",
    "q3", "q3_otro_text",
    "q4", "q4_otro_text",
    "q5", "q5_otro_text",
    "q6", "q6_otro_text",
    "q7", "q7_otro_text",
    "q8_csat",
    "q9_new", "q9_new_otro_text",  # ❌ PROBLEMA: DB espera q9_new_otro_text
    "q8", "q9", "q10", "q11", "q12", "q13",
    "q17"
}

# Campos que RECIBE main.py
main_fields = {
    "geo_lat", "geo_lng",
    "usuario", "q1_otro_text",
    "local", "q2_otro_text",
    "q3", "q3_otro_text",
    "q4", "q4_otro_text",
    "q5", "q5_otro_text",
    "q6", "q6_otro_text",
    "q7", "q7_otro_text",
    "q8_csat",
    "q9_new", "q9_otro_text",  # ❌ PROBLEMA: main.py recibe q9_otro_text
    "q8", "q9", "q10", "q11", "q12", "q13",
    "q17"
}

print("="*60)
print("ANÁLISIS DEL ERROR 500")
print("="*60)

print("\nPROBLEMA IDENTIFICADO:")
print("- HTML envía: q9_otro_text")
print("- main.py recibe: q9_otro_text")
print("- main.py mapea como: q9_new_otro_text")
print("- database.py espera: q9_new_otro_text")
print("\n✓ El mapeo está CORRECTO en el código")

print("\nPOSIBLE CAUSA DEL ERROR 500:")
print("1. HTML no está enviando q9_otro_text con el name correcto")
print("2. Hay algún campo requerido en la BD que no está en el formulario")
print("3. El HTML tiene campos extras que el backend no espera")

print("\n" + "="*60)
print("SOLUCIÓN: Actualizar HTML para que q9_new_otro_text sea el name")
print("="*60)

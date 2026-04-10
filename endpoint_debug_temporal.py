"""
ENDPOINT TEMPORAL DE DEBUG
Agregar a main.py para ver qué hay en la BD en producción
"""

@app.get("/admin/debug-bd")
def debug_bd(username: Annotated[str, Depends(verificar_credenciales)]):
    """Endpoint temporal para ver qué se guardó en BD."""
    from database import get_conn
    
    html = "<html><head><meta charset='utf-8'><title>Debug BD</title><style>"
    html += "body { font-family: monospace; padding: 20px; background: #f5f5f5; }"
    html += "table { border-collapse: collapse; background: white; }"
    html += "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }"
    html += "th { background: #0053e2; color: white; }"
    html += ".vacio { color: red; } .lleno { color: green; }"
    html += "</style></head><body>"
    html += "<h1>🔍 Debug BD - Última Visita</h1>"
    
    with get_conn() as conn:
        # Columnas
        columnas = conn.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'visitas'
            ORDER BY ordinal_position
        """).fetchall()
        
        html += f"<h2>✅ Columnas en tabla ({len(columnas)} total)</h2>"
        html += "<ol>"
        for col in columnas:
            html += f"<li>{col['column_name']}</li>"
        html += "</ol>"
        
        # Última visita
        visita = conn.execute("""
            SELECT * FROM visitas ORDER BY id DESC LIMIT 1
        """).fetchone()
        
        if visita:
            html += f"<h2>📊 Última Visita (ID {visita['id']})</h2>"
            html += "<table>"
            html += "<tr><th>Campo</th><th>Valor</th><th>Estado</th></tr>"
            
            for col in columnas:
                campo = col['column_name']
                valor = visita.get(campo, '')
                estado = '<span class="lleno">✅ Lleno</span>' if valor else '<span class="vacio">❌ Vacío</span>'
                html += f"<tr><td><strong>{campo}</strong></td><td>{valor or '(vacío)'}</td><td>{estado}</td></tr>"
            
            html += "</table>"
        else:
            html += "<p style='color:red;'>⚠️ NO HAY VISITAS EN LA BD</p>"
    
    html += "<br><a href='/dashboard'>← Volver al Dashboard</a>"
    html += "</body></html>"
    
    return HTMLResponse(content=html)

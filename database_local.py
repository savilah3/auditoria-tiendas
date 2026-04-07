"""
Database LOCAL con SQLite para uso en PC (sin PostgreSQL remoto)
"""
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict, Any
from pathlib import Path

TZ_CHILE = ZoneInfo("America/Santiago")

def now_chile() -> str:
    """Retorna la fecha y hora actual en zona horaria Chile (America/Santiago)."""
    return datetime.now(tz=TZ_CHILE).strftime("%Y-%m-%d %H:%M:%S")

# Database local SQLite
DB_PATH = Path("auditoria_local.db")

def get_conn():
    """Conexión a SQLite local"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Retornar dict en vez de tuplas
    return conn

def dict_from_row(row):
    """Convierte Row de SQLite a dict"""
    return dict(row) if row else None

def init_db() -> None:
    """Inicializa la base de datos SQLite local."""
    conn = get_conn()
    
    # Tabla Visitas con Sentido
    conn.execute("""
    CREATE TABLE IF NOT EXISTS visitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        geo_lat TEXT,
        geo_lng TEXT,
        usuario TEXT,
        local TEXT,
        -- Paso 1: Guardia
        q4a TEXT, q4a_other TEXT,
        q4b TEXT, q4b_other TEXT,
        -- Paso 1: Pasillos
        q5a TEXT, q5a_other TEXT,
        q5b TEXT, q5b_other TEXT,
        -- Paso 1: Colaborador
        q6 TEXT, q6_other TEXT,
        q8_resolutivo TEXT,
        comentarios_sala TEXT,
        -- Paso 2: Zona de pago
        tiempo_fila TEXT,
        q8_cajero_tipo TEXT,
        q9 TEXT,
        q10 TEXT,
        q11 TEXT,
        q12 TEXT,
        q13 TEXT,
        comentarios_pago TEXT,
        -- Paso 3: Comentarios finales
        q17 TEXT
    )
    """)
    
    # Entrevistas de Visitas
    conn.execute("""
    CREATE TABLE IF NOT EXISTS entrevistas_visitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visita_id INTEGER NOT NULL,
        numero_cliente INTEGER NOT NULL,
        motivo_visita TEXT,
        aspectos_positivos TEXT,
        oportunidades_mejora TEXT,
        FOREIGN KEY (visita_id) REFERENCES visitas(id) ON DELETE CASCADE
    )
    """)
    
    # Tabla Punto de Compra
    conn.execute("""
    CREATE TABLE IF NOT EXISTS punto_compra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        nombre TEXT,
        tienda TEXT,
        -- Step 1: Entrada
        s1_encontrar_punto TEXT,
        s1_observaciones TEXT,
        -- Step 2: Vitrinear
        s2_vitrinear TEXT,
        s2_comparar TEXT,
        s2_autonomo TEXT,
        s2_observaciones TEXT,
        -- Step 3: Selección
        s3_agregar_carro TEXT,
        s3_crear_usuario TEXT,
        s3_despacho_retiro TEXT,
        s3_observaciones TEXT,
        -- Step 4: Pago
        s4_medio_pago TEXT,
        s4_proceso_pago TEXT,
        s4_observaciones TEXT,
        -- Step 5: Espera
        s5_observaciones TEXT
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"[+] Base de datos SQLite creada: {DB_PATH.absolute()}")

def migrar_fechas_a_chile() -> dict:
    """No necesario en SQLite local, retorna status."""
    return {"estado": "no_requerido_sqlite", "conteos": {}}

# ============ Stats ============
def obtener_stats() -> dict:
    """Obtiene estadísticas generales."""
    conn = get_conn()
    
    total_punto_compra = conn.execute("SELECT COUNT(*) as total FROM punto_compra").fetchone()["total"]
    total_visitas = conn.execute("SELECT COUNT(*) as total FROM visitas").fetchone()["total"]
    
    conn.close()
    return {
        "total_punto_compra": total_punto_compra,
        "total_visitas": total_visitas,
    }

# ============ Punto de Compra ============
def insertar_punto_compra(data: dict) -> int:
    """Inserta evaluación punto de compra y retorna ID."""
    data["fecha"] = now_chile()
    conn = get_conn()
    
    cur = conn.execute("""
    INSERT INTO punto_compra (
        fecha, nombre, tienda,
        s1_encontrar_punto, s1_observaciones,
        s2_vitrinear, s2_comparar, s2_autonomo, s2_observaciones,
        s3_agregar_carro, s3_crear_usuario, s3_despacho_retiro, s3_observaciones,
        s4_medio_pago, s4_proceso_pago, s4_observaciones,
        s5_observaciones
    ) VALUES (
        :fecha, :nombre, :tienda,
        :s1_encontrar_punto, :s1_observaciones,
        :s2_vitrinear, :s2_comparar, :s2_autonomo, :s2_observaciones,
        :s3_agregar_carro, :s3_crear_usuario, :s3_despacho_retiro, :s3_observaciones,
        :s4_medio_pago, :s4_proceso_pago, :s4_observaciones,
        :s5_observaciones
    )
    """, data)
    
    row_id = cur.lastrowid
    conn.commit()
    conn.close()
    return row_id

def obtener_todas_punto_compra() -> List[Dict[str, Any]]:
    """Obtiene todas las evaluaciones punto de compra."""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM punto_compra ORDER BY fecha DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def eliminar_punto_compra(row_id: int) -> bool:
    """Elimina una evaluación punto de compra."""
    conn = get_conn()
    cur = conn.execute("DELETE FROM punto_compra WHERE id = ?", (row_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def limpiar_punto_compra() -> int:
    """Elimina TODOS los registros punto de compra."""
    conn = get_conn()
    cur = conn.execute("DELETE FROM punto_compra")
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return deleted

# ============ Visitas con Sentido ============
def insertar_visita(data: dict) -> int:
    """Inserta visita y retorna ID."""
    data["fecha"] = now_chile()
    conn = get_conn()
    
    cur = conn.execute("""
    INSERT INTO visitas (
        fecha, geo_lat, geo_lng, usuario, local,
        q4a, q4a_other, q4b, q4b_other,
        q5a, q5a_other, q5b, q5b_other,
        q6, q6_other, q8_resolutivo, comentarios_sala,
        tiempo_fila, q8_cajero_tipo, q9, q10, q11, q12, q13,
        comentarios_pago, q17
    ) VALUES (
        :fecha, :geo_lat, :geo_lng, :usuario, :local,
        :q4a, :q4a_other, :q4b, :q4b_other,
        :q5a, :q5a_other, :q5b, :q5b_other,
        :q6, :q6_other, :q8_resolutivo, :comentarios_sala,
        :tiempo_fila, :q8_cajero_tipo, :q9, :q10, :q11, :q12, :q13,
        :comentarios_pago, :q17
    )
    """, data)
    
    row_id = cur.lastrowid
    conn.commit()
    conn.close()
    return row_id

def insertar_entrevistas_visita(visita_id: int, entrevistas: List[Dict[str, str]]) -> None:
    """Inserta entrevistas de una visita."""
    if not entrevistas:
        return
    
    conn = get_conn()
    for i, e in enumerate(entrevistas, 1):
        conn.execute("""
        INSERT INTO entrevistas_visitas (
            visita_id, numero_cliente, motivo_visita,
            aspectos_positivos, oportunidades_mejora
        ) VALUES (?, ?, ?, ?, ?)
        """, (
            visita_id, i,
            e.get("motivo", ""),
            e.get("positivos", ""),
            e.get("oportunidades", "")
        ))
    conn.commit()
    conn.close()

def obtener_todas_visitas() -> List[Dict[str, Any]]:
    """Obtiene todas las visitas."""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM visitas ORDER BY fecha DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def obtener_entrevistas_visita(visita_id: int) -> List[Dict[str, Any]]:
    """Obtiene entrevistas de una visita."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM entrevistas_visitas WHERE visita_id = ? ORDER BY numero_cliente",
        (visita_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def eliminar_visita(row_id: int) -> bool:
    """Elimina una visita y sus entrevistas."""
    conn = get_conn()
    # SQLite CASCADE funciona si está habilitado
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.execute("DELETE FROM visitas WHERE id = ?", (row_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def limpiar_visitas() -> int:
    """Elimina TODOS los registros de visitas."""
    conn = get_conn()
    conn.execute("DELETE FROM entrevistas_visitas")
    cur = conn.execute("DELETE FROM visitas")
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return deleted

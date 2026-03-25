import os
import psycopg
import psycopg.rows
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import List, Dict, Any

TZ_CHILE = ZoneInfo("America/Santiago")


def now_chile() -> str:
    """Retorna la fecha y hora actual en zona horaria Chile (America/Santiago)."""
    return datetime.now(tz=TZ_CHILE).strftime("%Y-%m-%d %H:%M:%S")

DATABASE_URL = os.getenv("DATABASE_URL", "")

# Tabla principal de respuestas (auditoria)
CREATE_TABLE_RESPUESTAS = """
CREATE TABLE IF NOT EXISTS respuestas (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    formato TEXT,
    local TEXT,
    usuario TEXT,
    q4_guardia_saludo TEXT,
    q5_pasillos_saludo TEXT,
    q6_colaborador_resolutivo TEXT,
    q7_atencion_amable TEXT,
    q8_cajero_tipo TEXT,
    q9_cajero_saludo TEXT,
    q10_pmc TEXT,
    q11_lider_bci TEXT,
    q12_boleta_mail TEXT,
    q13_despedida TEXT,
    q17_comentarios TEXT
);
"""

# Nueva tabla para entrevistas a clientes (relacion 1:N con respuestas)
CREATE_TABLE_ENTREVISTAS = """
CREATE TABLE IF NOT EXISTS entrevistas_clientes (
    id SERIAL PRIMARY KEY,
    respuesta_id INTEGER NOT NULL REFERENCES respuestas(id) ON DELETE CASCADE,
    numero_cliente INTEGER NOT NULL,
    q14_motivo_visita TEXT,
    q15_aspectos_positivos TEXT,
    q16_oportunidades_mejora TEXT
);
"""

# Tabla para checklist de Atención v2 (campos nuevos del formulario Visitas con Sentido)
CREATE_TABLE_ATENCION = """
CREATE TABLE IF NOT EXISTS atencion (
    id SERIAL PRIMARY KEY,
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
    q9 TEXT, q10 TEXT, q11 TEXT, q12 TEXT, q13 TEXT,
    comentarios_pago TEXT,
    -- Paso 3: Comentarios finales
    q17 TEXT
);
"""

# Tabla para entrevistas de Atención (relacion 1:N)
CREATE_TABLE_ENTREVISTAS_ATENCION = """
CREATE TABLE IF NOT EXISTS entrevistas_atencion (
    id SERIAL PRIMARY KEY,
    atencion_id INTEGER NOT NULL REFERENCES atencion(id) ON DELETE CASCADE,
    numero_cliente INTEGER NOT NULL,
    motivo_visita TEXT,
    aspectos_positivos TEXT,
    oportunidades_mejora TEXT
);
"""

# Tabla para "Visitas con Sentido" (nuevo formulario)
CREATE_TABLE_VISITAS = """
CREATE TABLE IF NOT EXISTS visitas (
    id SERIAL PRIMARY KEY,
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
    -- Paso 1: Colaborador resolutivo
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
);
"""

CREATE_TABLE_ENTREVISTAS_VISITAS = """
CREATE TABLE IF NOT EXISTS entrevistas_visitas (
    id SERIAL PRIMARY KEY,
    visita_id INTEGER NOT NULL REFERENCES visitas(id) ON DELETE CASCADE,
    numero_cliente INTEGER NOT NULL,
    motivo_visita TEXT,
    aspectos_positivos TEXT,
    oportunidades_mejora TEXT
);
"""



CREATE_TABLE_PUNTO_COMPRA = """
CREATE TABLE IF NOT EXISTS punto_compra (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    nombre TEXT,
    tienda TEXT,
    -- Step 1: Encuentra el sector
    s1_encontrar_sector TEXT,
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
    s4_pan_caja TEXT,
    s4_observaciones TEXT,
    -- Step 5: Espera
    s5_observaciones TEXT
);
"""


def get_conn():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=psycopg.rows.dict_row,
        sslmode="require",
    )


def init_db() -> None:
    """Inicializa las tablas y ejecuta migraciones necesarias."""
    with get_conn() as conn:
        # Crear tablas
        conn.execute(CREATE_TABLE_RESPUESTAS)
        conn.execute(CREATE_TABLE_ENTREVISTAS)
        conn.execute(CREATE_TABLE_ATENCION)
        conn.execute(CREATE_TABLE_ENTREVISTAS_ATENCION)
        conn.execute(CREATE_TABLE_PUNTO_COMPRA)
        conn.execute(CREATE_TABLE_VISITAS)
        conn.execute(CREATE_TABLE_ENTREVISTAS_VISITAS)

        # Migracion: recrear tabla atencion si tiene esquema viejo (sin columna q4a)
        old_schema = conn.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'atencion' AND column_name = 'q4_guardia_3m'
        """).fetchone()
        if old_schema:
            conn.execute("DROP TABLE IF EXISTS entrevistas_atencion CASCADE")
            conn.execute("DROP TABLE IF EXISTS atencion CASCADE")
            conn.execute(CREATE_TABLE_ATENCION)
            conn.execute(CREATE_TABLE_ENTREVISTAS_ATENCION)
        
        # Migracion: renombrar 'rut' a 'usuario' si existe
        row = conn.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'respuestas' AND column_name = 'rut'
        """).fetchone()
        if row:
            conn.execute("ALTER TABLE respuestas RENAME COLUMN rut TO usuario")
        
        # Migracion: renombrar q14_comentarios a q17_comentarios si existe
        row = conn.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'respuestas' AND column_name = 'q14_comentarios'
        """).fetchone()
        if row:
            conn.execute("ALTER TABLE respuestas RENAME COLUMN q14_comentarios TO q17_comentarios")
        
        # Migracion: agregar q17_comentarios si no existe
        row = conn.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'respuestas' AND column_name = 'q17_comentarios'
        """).fetchone()
        if not row:
            conn.execute("ALTER TABLE respuestas ADD COLUMN q17_comentarios TEXT")
        
        conn.commit()


# ─── Migración: corregir fechas UTC → hora Chile ─────────────────────────

CREATE_TABLE_MIGRACIONES = """
CREATE TABLE IF NOT EXISTS migraciones (
    nombre TEXT PRIMARY KEY,
    aplicada_en TEXT NOT NULL
);
"""


def _migracion_aplicada(conn, nombre: str) -> bool:
    """Comprueba si una migración ya fue aplicada."""
    conn.execute(CREATE_TABLE_MIGRACIONES)
    row = conn.execute(
        "SELECT nombre FROM migraciones WHERE nombre = %s", (nombre,)
    ).fetchone()
    return row is not None


def _marcar_migracion(conn, nombre: str) -> None:
    """Registra la migración como aplicada."""
    conn.execute(
        "INSERT INTO migraciones (nombre, aplicada_en) VALUES (%s, %s)",
        (nombre, now_chile()),
    )


def _convertir_utc_a_chile(fecha_str: str) -> str:
    """Convierte un string 'YYYY-MM-DD HH:MM:SS' interpretado como UTC a hora Chile."""
    try:
        dt_utc = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        )
        dt_chile = dt_utc.astimezone(TZ_CHILE)
        return dt_chile.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return fecha_str  # Si el formato falla, dejar como está


def migrar_fechas_a_chile() -> dict:
    """Convierte fechas UTC → hora Chile en todas las tablas. Solo se ejecuta una vez."""
    MIGRATION_NAME = "utc_to_chile_tz_v1"
    tablas = ["respuestas", "punto_compra", "atencion", "visitas"]
    conteos: Dict[str, int] = {t: 0 for t in tablas}

    with get_conn() as conn:
        if _migracion_aplicada(conn, MIGRATION_NAME):
            return {"estado": "ya_aplicada", "conteos": conteos}

        for tabla in tablas:
            rows = conn.execute(f"SELECT id, fecha FROM {tabla}").fetchall()
            for row in rows:
                nueva_fecha = _convertir_utc_a_chile(row["fecha"])
                if nueva_fecha != row["fecha"]:
                    conn.execute(
                        f"UPDATE {tabla} SET fecha = %s WHERE id = %s",
                        (nueva_fecha, row["id"]),
                    )
                    conteos[tabla] += 1

        _marcar_migracion(conn, MIGRATION_NAME)
        conn.commit()

    return {"estado": "aplicada", "conteos": conteos}


# ============ Funciones de limpieza masiva ============

def limpiar_visitas() -> int:
    """Elimina TODOS los registros de visitas y sus entrevistas. Retorna el número de visitas borradas."""
    with get_conn() as conn:
        conn.execute("DELETE FROM entrevistas_visitas")
        cur = conn.execute("DELETE FROM visitas")
        deleted = cur.rowcount
        conn.commit()
    return deleted


def limpiar_punto_compra() -> int:
    """Elimina TODOS los registros de punto de compra. Retorna el número de filas borradas."""
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM punto_compra")
        deleted = cur.rowcount
        conn.commit()
    return deleted


def obtener_stats() -> dict:
    """Obtiene estadísticas generales."""
    with get_conn() as conn:
        total_punto_compra = conn.execute(
            "SELECT COUNT(*) as total FROM punto_compra"
        ).fetchone()["total"]

        total_visitas = conn.execute(
            "SELECT COUNT(*) as total FROM visitas"
        ).fetchone()["total"]

    return {
        "total_punto_compra": total_punto_compra,
        "total_visitas": total_visitas,
    }


# ============ Funciones para Punto de Compra ============

def insertar_punto_compra(data: dict) -> int:
    """Inserta una evaluación de punto de compra y retorna el ID."""
    data["fecha"] = now_chile()
    sql = """
    INSERT INTO punto_compra (
        fecha, nombre, tienda,
        s1_encontrar_sector, s1_encontrar_punto, s1_observaciones,
        s2_vitrinear, s2_comparar, s2_autonomo, s2_observaciones,
        s3_agregar_carro, s3_crear_usuario, s3_despacho_retiro, s3_observaciones,
        s4_medio_pago, s4_proceso_pago, s4_pan_caja, s4_observaciones,
        s5_observaciones
    ) VALUES (
        %(fecha)s, %(nombre)s, %(tienda)s,
        %(s1_encontrar_sector)s, %(s1_encontrar_punto)s, %(s1_observaciones)s,
        %(s2_vitrinear)s, %(s2_comparar)s, %(s2_autonomo)s, %(s2_observaciones)s,
        %(s3_agregar_carro)s, %(s3_crear_usuario)s, %(s3_despacho_retiro)s, %(s3_observaciones)s,
        %(s4_medio_pago)s, %(s4_proceso_pago)s, %(s4_pan_caja)s, %(s4_observaciones)s,
        %(s5_observaciones)s
    )
    RETURNING id
    """
    with get_conn() as conn:
        result = conn.execute(sql, data).fetchone()
        conn.commit()
        return result["id"]


def obtener_todas_punto_compra() -> List[Dict[str, Any]]:
    """Obtiene todas las evaluaciones de punto de compra."""
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM punto_compra ORDER BY fecha DESC"
        ).fetchall()


def eliminar_punto_compra(row_id: int) -> bool:
    """Elimina una evaluación de punto de compra."""
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM punto_compra WHERE id = %s", (row_id,))
        deleted = cur.rowcount > 0
        conn.commit()
    return deleted


# ============ Funciones para Visitas con Sentido ============

def insertar_visita(data: dict) -> int:
    """Inserta una visita y retorna el ID generado."""
    data["fecha"] = now_chile()
    sql = """
    INSERT INTO visitas (
        fecha, geo_lat, geo_lng, usuario, local,
        q4a, q4a_other, q4b, q4b_other,
        q5a, q5a_other, q5b, q5b_other,
        q6, q6_other, q8_resolutivo, comentarios_sala,
        tiempo_fila, q8_cajero_tipo, q9, q10, q11, q12, q13,
        comentarios_pago, q17
    ) VALUES (
        %(fecha)s, %(geo_lat)s, %(geo_lng)s, %(usuario)s, %(local)s,
        %(q4a)s, %(q4a_other)s, %(q4b)s, %(q4b_other)s,
        %(q5a)s, %(q5a_other)s, %(q5b)s, %(q5b_other)s,
        %(q6)s, %(q6_other)s, %(q8_resolutivo)s, %(comentarios_sala)s,
        %(tiempo_fila)s, %(q8_cajero_tipo)s, %(q9)s, %(q10)s, %(q11)s, %(q12)s, %(q13)s,
        %(comentarios_pago)s, %(q17)s
    )
    RETURNING id
    """
    with get_conn() as conn:
        result = conn.execute(sql, data).fetchone()
        conn.commit()
        return result["id"]


def insertar_entrevistas_visita(visita_id: int, entrevistas: List[Dict[str, str]]) -> None:
    """Inserta las entrevistas de clientes de una visita."""
    if not entrevistas:
        return
    sql = """
    INSERT INTO entrevistas_visitas (
        visita_id, numero_cliente, motivo_visita, aspectos_positivos, oportunidades_mejora
    ) VALUES (
        %(visita_id)s, %(numero_cliente)s, %(motivo_visita)s,
        %(aspectos_positivos)s, %(oportunidades_mejora)s
    )
    """
    with get_conn() as conn:
        for i, e in enumerate(entrevistas, 1):
            conn.execute(sql, {
                "visita_id": visita_id,
                "numero_cliente": i,
                "motivo_visita": e.get("motivo", ""),
                "aspectos_positivos": e.get("positivos", ""),
                "oportunidades_mejora": e.get("oportunidades", ""),
            })
        conn.commit()


def obtener_todas_visitas() -> List[Dict[str, Any]]:
    """Obtiene todas las visitas ordenadas por fecha."""
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM visitas ORDER BY fecha DESC"
        ).fetchall()


def obtener_entrevistas_visita(visita_id: int) -> List[Dict[str, Any]]:
    """Obtiene las entrevistas de una visita."""
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM entrevistas_visitas WHERE visita_id = %s ORDER BY numero_cliente",
            (visita_id,)
        ).fetchall()


def eliminar_visita(row_id: int) -> bool:
    """Elimina una visita y sus entrevistas (CASCADE)."""
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM visitas WHERE id = %s", (row_id,))
        deleted = cur.rowcount > 0
        conn.commit()
    return deleted

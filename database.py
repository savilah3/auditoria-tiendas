import os
import psycopg
import psycopg.rows
from datetime import datetime
from typing import List, Dict, Any

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


def insertar_respuesta(data: dict) -> int:
    """Inserta una respuesta y retorna el ID generado."""
    data["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """
    INSERT INTO respuestas (
        fecha, formato, local, usuario,
        q4_guardia_saludo, q5_pasillos_saludo, q6_colaborador_resolutivo,
        q7_atencion_amable, q8_cajero_tipo, q9_cajero_saludo,
        q10_pmc, q11_lider_bci, q12_boleta_mail, q13_despedida,
        q17_comentarios
    ) VALUES (
        %(fecha)s, %(formato)s, %(local)s, %(usuario)s,
        %(q4_guardia_saludo)s, %(q5_pasillos_saludo)s, %(q6_colaborador_resolutivo)s,
        %(q7_atencion_amable)s, %(q8_cajero_tipo)s, %(q9_cajero_saludo)s,
        %(q10_pmc)s, %(q11_lider_bci)s, %(q12_boleta_mail)s, %(q13_despedida)s,
        %(q17_comentarios)s
    )
    RETURNING id
    """
    with get_conn() as conn:
        result = conn.execute(sql, data).fetchone()
        conn.commit()
        return result["id"]


def insertar_entrevistas(respuesta_id: int, entrevistas: List[Dict[str, str]]) -> None:
    """Inserta las entrevistas a clientes asociadas a una respuesta."""
    if not entrevistas:
        return
    
    sql = """
    INSERT INTO entrevistas_clientes (
        respuesta_id, numero_cliente,
        q14_motivo_visita, q15_aspectos_positivos, q16_oportunidades_mejora
    ) VALUES (
        %(respuesta_id)s, %(numero_cliente)s,
        %(q14_motivo_visita)s, %(q15_aspectos_positivos)s, %(q16_oportunidades_mejora)s
    )
    """
    with get_conn() as conn:
        for i, entrevista in enumerate(entrevistas, 1):
            conn.execute(sql, {
                "respuesta_id": respuesta_id,
                "numero_cliente": i,
                "q14_motivo_visita": entrevista.get("motivo", ""),
                "q15_aspectos_positivos": entrevista.get("positivos", ""),
                "q16_oportunidades_mejora": entrevista.get("oportunidades", ""),
            })
        conn.commit()


def obtener_todas() -> List[Dict[str, Any]]:
    """Obtiene todas las respuestas ordenadas por fecha."""
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM respuestas ORDER BY fecha DESC"
        ).fetchall()


def obtener_entrevistas(respuesta_id: int) -> List[Dict[str, Any]]:
    """Obtiene las entrevistas de una respuesta especifica."""
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM entrevistas_clientes WHERE respuesta_id = %s ORDER BY numero_cliente",
            (respuesta_id,)
        ).fetchall()


def obtener_respuesta_con_entrevistas(respuesta_id: int) -> Dict[str, Any] | None:
    """Obtiene una respuesta con sus entrevistas."""
    with get_conn() as conn:
        respuesta = conn.execute(
            "SELECT * FROM respuestas WHERE id = %s", (respuesta_id,)
        ).fetchone()
        
        if not respuesta:
            return None
        
        entrevistas = conn.execute(
            "SELECT * FROM entrevistas_clientes WHERE respuesta_id = %s ORDER BY numero_cliente",
            (respuesta_id,)
        ).fetchall()
        
        return {**respuesta, "entrevistas": entrevistas}


def eliminar_respuesta(row_id: int) -> bool:
    """Elimina una respuesta y sus entrevistas asociadas (CASCADE)."""
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM respuestas WHERE id = %s", (row_id,))
        deleted = cur.rowcount > 0
        conn.commit()
    return deleted


def obtener_stats() -> dict:
    """Obtiene estadisticas generales."""
    with get_conn() as conn:
        total = conn.execute(
            "SELECT COUNT(*) as total FROM respuestas"
        ).fetchone()["total"]
        
        por_formato = [
            (r["formato"], r["cnt"])
            for r in conn.execute(
                "SELECT formato, COUNT(*) as cnt FROM respuestas GROUP BY formato"
            ).fetchall()
        ]
        
        total_entrevistas = conn.execute(
            "SELECT COUNT(*) as total FROM entrevistas_clientes"
        ).fetchone()["total"]
        
    return {
        "total": total,
        "por_formato": por_formato,
        "total_entrevistas": total_entrevistas,
    }

import os
import psycopg
import psycopg.rows
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "")

CREATE_TABLE = """
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
    q14_comentarios TEXT
);
"""


def get_conn():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=psycopg.rows.dict_row,
        sslmode="require",
    )


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(CREATE_TABLE)
        # Migracion: renombrar 'rut' a 'usuario' si existe
        row = conn.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'respuestas' AND column_name = 'rut'
        """).fetchone()
        if row:
            conn.execute("ALTER TABLE respuestas RENAME COLUMN rut TO usuario")
        conn.commit()


def insertar_respuesta(data: dict) -> None:
    data["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """
    INSERT INTO respuestas (
        fecha, formato, local, usuario,
        q4_guardia_saludo, q5_pasillos_saludo, q6_colaborador_resolutivo,
        q7_atencion_amable, q8_cajero_tipo, q9_cajero_saludo,
        q10_pmc, q11_lider_bci, q12_boleta_mail, q13_despedida,
        q14_comentarios
    ) VALUES (
        %(fecha)s, %(formato)s, %(local)s, %(usuario)s,
        %(q4_guardia_saludo)s, %(q5_pasillos_saludo)s, %(q6_colaborador_resolutivo)s,
        %(q7_atencion_amable)s, %(q8_cajero_tipo)s, %(q9_cajero_saludo)s,
        %(q10_pmc)s, %(q11_lider_bci)s, %(q12_boleta_mail)s, %(q13_despedida)s,
        %(q14_comentarios)s
    )
    """
    with get_conn() as conn:
        conn.execute(sql, data)
        conn.commit()


def obtener_todas() -> list:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM respuestas ORDER BY fecha DESC"
        ).fetchall()


def eliminar_respuesta(row_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM respuestas WHERE id = %s", (row_id,))
        deleted = cur.rowcount > 0
        conn.commit()
    return deleted


def obtener_stats() -> dict:
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
    return {"total": total, "por_formato": por_formato}

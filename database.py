import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("auditoria.db")

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS respuestas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    formato TEXT,
    local TEXT,
    rut TEXT,
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


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(CREATE_TABLE)


def insertar_respuesta(data: dict) -> int:
    sql = """
    INSERT INTO respuestas (
        fecha, formato, local, rut,
        q4_guardia_saludo, q5_pasillos_saludo, q6_colaborador_resolutivo,
        q7_atencion_amable, q8_cajero_tipo, q9_cajero_saludo,
        q10_pmc, q11_lider_bci, q12_boleta_mail, q13_despedida,
        q14_comentarios
    ) VALUES (
        :fecha, :formato, :local, :rut,
        :q4_guardia_saludo, :q5_pasillos_saludo, :q6_colaborador_resolutivo,
        :q7_atencion_amable, :q8_cajero_tipo, :q9_cajero_saludo,
        :q10_pmc, :q11_lider_bci, :q12_boleta_mail, :q13_despedida,
        :q14_comentarios
    )
    """
    data["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_conn() as conn:
        cursor = conn.execute(sql, data)
        return cursor.lastrowid


def obtener_todas() -> list[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM respuestas ORDER BY fecha DESC"
        ).fetchall()


def obtener_stats() -> dict:
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM respuestas").fetchone()[0]
        por_formato = conn.execute(
            "SELECT formato, COUNT(*) as cnt FROM respuestas GROUP BY formato"
        ).fetchall()
        return {
            "total": total,
            "por_formato": [(r["formato"], r["cnt"]) for r in por_formato],
        }

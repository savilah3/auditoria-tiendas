"""
Single source of truth para los formularios "Pick Up y Devoluciones".

Cada CANAL (SOD, Marketplace, CATEX) se define UNA sola vez aqui: sus pasos,
preguntas (con nombre de columna descriptivo + descripcion legible) y campos
de observaciones. A partir de esta config se generan automaticamente:

    * El DDL de la tabla (CREATE TABLE ... TEXT por campo)
    * El INSERT con parametros nombrados de psycopg
    * Las columnas del dashboard
    * Las hojas/headers del Excel

Asi es imposible que un campo se guarde sin salir en el dashboard o el Excel:
todos derivan de la misma lista. (Zen de Python: "There should be one obvious
way to do it".)

Los `name` de cada pregunta DEBEN coincidir con los `name` de los radios en el
HTML del canal (templates/pu_devoluciones_*.html). Si tocas uno, toca el otro.
"""
from typing import Dict, List, Tuple

# Una pregunta = (nombre_columna, descripcion_legible)
Pregunta = Tuple[str, str]


class Step:
    """Un paso del formulario: titulo + preguntas (radios) + campo observaciones."""

    def __init__(self, num: int, title: str, preguntas: List[Pregunta], obs: str):
        self.num = num
        self.title = title
        self.preguntas = preguntas
        self.obs = obs  # nombre de columna del textarea de observaciones


class Channel:
    """Un canal completo de Pick Up y Devoluciones."""

    def __init__(
        self,
        key: str,
        label: str,
        table: str,
        route: str,
        template: str,
        steps: List[Step],
    ):
        self.key = key            # "sod" | "marketplace" | "catex"
        self.label = label        # nombre para mostrar en dashboard/excel
        self.table = table        # tabla Postgres
        self.route = route        # ruta GET del formulario (sin slash inicial)
        self.template = template  # archivo en templates/
        self.steps = steps

    # ---- Derivados (single source of truth) ----
    @property
    def submit_route(self) -> str:
        return f"/submit-{self.route}"

    @property
    def gracias_route(self) -> str:
        return f"/gracias-{self.route}"

    @property
    def tab(self) -> str:
        return self.route

    def columns(self) -> List[str]:
        """Todas las columnas de datos en orden (sin id ni fecha)."""
        cols: List[str] = ["nombre"]
        for step in self.steps:
            cols.extend(name for name, _ in step.preguntas)
            cols.append(step.obs)
        return cols

    def headers(self) -> List[Tuple[str, str]]:
        """(columna, header_legible) para dashboard y Excel."""
        out: List[Tuple[str, str]] = [("nombre", "Nombre Lider")]
        for step in self.steps:
            for name, desc in step.preguntas:
                out.append((name, f"[P{step.num}] {desc}"))
            out.append((step.obs, f"[P{step.num}] Observaciones"))
        return out

    def create_table_sql(self) -> str:
        cols_ddl = ",\n    ".join(f"{c} TEXT" for c in self.columns())
        return (
            f"CREATE TABLE IF NOT EXISTS {self.table} (\n"
            f"    id SERIAL PRIMARY KEY,\n"
            f"    fecha TEXT NOT NULL,\n"
            f"    {cols_ddl}\n"
            f");"
        )

    def insert_sql(self) -> str:
        cols = ["fecha"] + self.columns()
        col_list = ", ".join(cols)
        val_list = ", ".join(f"%({c})s" for c in cols)
        return (
            f"INSERT INTO {self.table} ({col_list}) "
            f"VALUES ({val_list}) RETURNING id"
        )


# ─── Preguntas compartidas (Pick Up y Devolucion son identicas en los 3) ───
PICKUP = [
    ("s4_ubicacion_pickup", "Claridad de la ubicacion zona Pick Up"),
    ("s4_tiempo_espera", "Tiempos de espera para recibir el pedido (promesa 5 minutos)"),
    ("s4_atencion_personal", "Atencion y disposicion resolutiva del personal"),
    ("s4_estado_pedido", "Recepcion y estado del pedido"),
]
DEVOLUCION = [
    ("s5_info_devolucion", "Accesibilidad y claridad de la informacion para realizar la devolucion"),
    ("s5_opciones_devolucion", "Disponibilidad de opciones para el cambio o devolucion del producto"),
    ("s5_proceso_devolucion", "Proceso de devolucion de dinero"),
    ("s5_atencion_colaborador", "Amabilidad y disposicion en la atencion del colaborador y/o ejecutivo contact center"),
]


CHANNELS: Dict[str, Channel] = {
    "sod": Channel(
        key="sod",
        label="Pick Up y Devoluciones · SOD",
        table="pu_devoluciones",
        route="pu-devoluciones",
        template="pu_devoluciones_sod.html",
        steps=[
            Step(1, "Compra en Lider.cl", [
                ("s1_busqueda", "Busqueda de los productos en la web"),
                ("s1_info_producto", "Claridad y disponibilidad de informacion del producto en la web"),
                ("s1_comparar_productos", "Facilidad para comparar productos (Ej. formatos, precio por kilo)"),
                ("s1_conveniencia_precios", "Claridad Conveniencia de Precios"),
                ("s1_retiro_tienda", "Seleccion de la opcion 'Retiro en Tienda' y eleccion del local"),
                ("s1_proceso_pago", "Facilidad del proceso de pago"),
            ], obs="s1_obs"),
            Step(3, "Espera", [
                ("s3_info_estado_pedido", "Claridad de la informacion recibida sobre el estado del pedido"),
                ("s3_gestion_sustituciones", "Gestion y comunicacion de sustituciones de productos (si aplica)"),
            ], obs="s3_obs"),
            Step(4, "Pick Up", PICKUP, obs="s4_obs"),
            Step(5, "Devolucion", DEVOLUCION, obs="s5_obs"),
        ],
    ),
    "marketplace": Channel(
        key="marketplace",
        label="Pick Up y Devoluciones · Marketplace",
        table="pu_marketplace",
        route="pu-devoluciones-marketplace",
        template="pu_devoluciones_marketplace.html",
        steps=[
            Step(1, "Compra en Lider.cl", [
                ("s1_busqueda", "Busqueda de los productos en la web (lavadora y neumaticos)"),
                ("s1_info_producto", "Claridad y disponibilidad de informacion de los productos en la web"),
                ("s1_identificacion_terceros", "Identificacion clara de que los productos eran vendidos por terceros"),
                ("s1_plazos_retiro", "Claridad en los plazos de retiro estipulados para estos productos"),
                ("s1_retiro_tienda", "Seleccion de la opcion 'Retiro en Tienda' y eleccion del local"),
                ("s1_proceso_pago", "Facilidad del proceso de pago"),
            ], obs="s1_obs"),
            Step(3, "Espera", [
                ("s3_info_estado_pedido", "Claridad de la informacion recibida sobre el estado del pedido"),
            ], obs="s3_obs"),
            Step(4, "Pick Up", PICKUP, obs="s4_obs"),
            Step(5, "Devolucion", DEVOLUCION, obs="s5_obs"),
        ],
    ),
    "catex": Channel(
        key="catex",
        label="Pick Up y Devoluciones · CATEX",
        table="pu_catex",
        route="pu-devoluciones-catex",
        template="pu_devoluciones_catex.html",
        steps=[
            Step(1, "Compra en Lider.cl", [
                ("s1_busqueda", "Busqueda de los productos en la web (microondas y plancha)"),
                ("s1_info_producto", "Claridad y disponibilidad de informacion de los productos en la web"),
                ("s1_disponibilidad_retiro", "Disponibilidad de retiro para los productos en tu local"),
                ("s1_retiro_tienda", "Seleccion de la opcion 'Retiro en Tienda' y eleccion del local"),
                ("s1_proceso_pago", "Facilidad del proceso de pago"),
            ], obs="s1_obs"),
            Step(3, "Espera", [
                ("s3_info_estado_pedido", "Claridad de la informacion recibida sobre el estado del pedido"),
            ], obs="s3_obs"),
            Step(4, "Pick Up", PICKUP, obs="s4_obs"),
            Step(5, "Devolucion", DEVOLUCION, obs="s5_obs"),
        ],
    ),
}

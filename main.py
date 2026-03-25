import io
import json
import os
import secrets
from typing import Annotated, List

import openpyxl
from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from database import (
    init_db,
    migrar_fechas_a_chile,
    obtener_stats,
    insertar_punto_compra,
    obtener_todas_punto_compra,
    eliminar_punto_compra,
    insertar_visita,
    insertar_entrevistas_visita,
    obtener_todas_visitas,
    obtener_entrevistas_visita,
    eliminar_visita,
    limpiar_visitas,
    limpiar_punto_compra,
)

app = FastAPI(title="En los zapatos del cliente")
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

# Credenciales del dashboard (configurar en Render como env vars)
DASHBOARD_USER = os.getenv("DASHBOARD_USER", "admin")
DASHBOARD_PASS = os.getenv("DASHBOARD_PASS", "walmart2025")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    resultado = migrar_fechas_a_chile()
    print(f"[TZ Migration] {resultado}")


# --- Autenticacion basica para el dashboard ---
def verificar_credenciales(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    user_ok = secrets.compare_digest(credentials.username, DASHBOARD_USER)
    pass_ok = secrets.compare_digest(credentials.password, DASHBOARD_PASS)
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# --- Redireccion raiz ---
@app.get("/", response_class=HTMLResponse)
def raiz(request: Request):
    return RedirectResponse(url="/visitas", status_code=302)


# --- Formulario Punto de Compra ---
@app.get("/punto-compra", response_class=HTMLResponse)
def mostrar_punto_compra(request: Request):
    """Formulario de evaluación Punto de Compra."""
    return templates.TemplateResponse("punto_compra.html", {"request": request})


@app.post("/submit-punto-compra")
def recibir_punto_compra(
    nombre: Annotated[str, Form()] = "",
    tienda: Annotated[str, Form()] = "",
    # Step 1
    s1_i1: Annotated[str, Form()] = "",
    s1_i2: Annotated[str, Form()] = "",
    s1_obs: Annotated[str, Form()] = "",
    # Step 2
    s2_i1: Annotated[str, Form()] = "",
    s2_i2: Annotated[str, Form()] = "",
    s2_i3: Annotated[str, Form()] = "",
    s2_obs: Annotated[str, Form()] = "",
    # Step 3
    s3_i1: Annotated[str, Form()] = "",
    s3_i4: Annotated[str, Form()] = "",
    s3_i3: Annotated[str, Form()] = "",
    s3_obs: Annotated[str, Form()] = "",
    # Step 4
    s4_i1: Annotated[str, Form()] = "",
    s4_i2: Annotated[str, Form()] = "",
    s4_i3: Annotated[str, Form()] = "",
    s4_obs: Annotated[str, Form()] = "",
    # Step 5
    s5_obs: Annotated[str, Form()] = "",
):
    """Recibe la evaluación de punto de compra."""
    insertar_punto_compra({
        "nombre": nombre,
        "tienda": tienda,
        "s1_encontrar_sector": s1_i1,
        "s1_encontrar_punto": s1_i2,
        "s1_observaciones": s1_obs,
        "s2_vitrinear": s2_i1,
        "s2_comparar": s2_i2,
        "s2_autonomo": s2_i3,
        "s2_observaciones": s2_obs,
        "s3_agregar_carro": s3_i1,
        "s3_crear_usuario": s3_i4,
        "s3_despacho_retiro": s3_i3,
        "s3_observaciones": s3_obs,
        "s4_medio_pago": s4_i1,
        "s4_proceso_pago": s4_i2,
        "s4_pan_caja": s4_i3,
        "s4_observaciones": s4_obs,
        "s5_observaciones": s5_obs,
    })
    return RedirectResponse(url="/gracias-punto-compra", status_code=303)


@app.get("/gracias-punto-compra", response_class=HTMLResponse)
def gracias_punto_compra(request: Request):
    return templates.TemplateResponse("gracias_punto_compra.html", {"request": request})


# --- Formulario Visitas con Sentido ---
@app.get("/visitas", response_class=HTMLResponse)
def mostrar_visitas(request: Request):
    """Formulario Visitas con Sentido."""
    return templates.TemplateResponse("visitas.html", {"request": request})


@app.post("/submit-visita")
def recibir_visita(
    geo_lat: Annotated[str, Form()] = "",
    geo_lng: Annotated[str, Form()] = "",
    usuario: Annotated[str, Form()] = "",
    local: Annotated[str, Form()] = "",
    local_otro: Annotated[str, Form()] = "",
    # Paso 1: Guardia
    q4a: Annotated[str, Form()] = "",
    q4a_other: Annotated[str, Form()] = "",
    q4b: Annotated[str, Form()] = "",
    q4b_other: Annotated[str, Form()] = "",
    # Paso 1: Pasillos
    q5a: Annotated[str, Form()] = "",
    q5a_other: Annotated[str, Form()] = "",
    q5b: Annotated[str, Form()] = "",
    q5b_other: Annotated[str, Form()] = "",
    # Paso 1: Colaborador
    q6: Annotated[str, Form()] = "",
    q6_other: Annotated[str, Form()] = "",
    q8_resolutivo: Annotated[str, Form()] = "",
    comentarios_sala: Annotated[str, Form()] = "",
    # Paso 2: Zona de pago
    tiempo_fila: Annotated[str, Form()] = "",
    q8_cajero_tipo: Annotated[str, Form()] = "",
    q9: Annotated[str, Form()] = "",
    q10: Annotated[str, Form()] = "",
    q11: Annotated[str, Form()] = "",
    q12: Annotated[str, Form()] = "",
    q13: Annotated[str, Form()] = "",
    comentarios_pago: Annotated[str, Form()] = "",
    # Paso 3: Comentarios finales
    q17: Annotated[str, Form()] = "",
    entrevistas_json: Annotated[str, Form()] = "[]",
):
    """Recibe el formulario Visitas con Sentido."""
    # Si seleccionó "otro", usar el texto libre como local
    local_final = local_otro.strip() if local == "otro" and local_otro.strip() else local
    visita_id = insertar_visita({
        "geo_lat": geo_lat,
        "geo_lng": geo_lng,
        "usuario": usuario,
        "local": local_final,
        "q4a": q4a, "q4a_other": q4a_other,
        "q4b": q4b, "q4b_other": q4b_other,
        "q5a": q5a, "q5a_other": q5a_other,
        "q5b": q5b, "q5b_other": q5b_other,
        "q6": q6, "q6_other": q6_other,
        "q8_resolutivo": q8_resolutivo,
        "comentarios_sala": comentarios_sala,
        "tiempo_fila": tiempo_fila,
        "q8_cajero_tipo": q8_cajero_tipo,
        "q9": q9, "q10": q10, "q11": q11,
        "q12": q12, "q13": q13,
        "comentarios_pago": comentarios_pago,
        "q17": q17,
    })
    try:
        entrevistas = json.loads(entrevistas_json)
        if isinstance(entrevistas, list):
            insertar_entrevistas_visita(visita_id, entrevistas)
    except json.JSONDecodeError:
        pass
    return RedirectResponse(url="/gracias", status_code=303)



@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    _: Annotated[str, Depends(verificar_credenciales)],
    tab: str = "visitas",
):
    # Obtener datos de punto de compra
    punto_compra_rows = obtener_todas_punto_compra()

    # Obtener datos de Visitas con Sentido
    visita_rows = obtener_todas_visitas()
    visitas_con_entrevistas = []
    for row in visita_rows:
        entrevistas = obtener_entrevistas_visita(row["id"])
        visitas_con_entrevistas.append({**row, "entrevistas": entrevistas})

    stats = obtener_stats()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "rows": visitas_con_entrevistas,
            "punto_compra_rows": punto_compra_rows,
            "visita_rows": visitas_con_entrevistas,
            "stats": stats,
            "tab": tab,
        },
    )


@app.post("/dashboard/delete-punto-compra/{row_id}")
def eliminar_pc(
    row_id: int,
    _: Annotated[str, Depends(verificar_credenciales)],
):
    """Elimina una evaluación de punto de compra."""
    eliminar_punto_compra(row_id)
    return RedirectResponse(url="/dashboard?tab=punto-compra", status_code=303)


@app.post("/dashboard/delete-visita/{row_id}")
def eliminar_visita_endpoint(
    row_id: int,
    _: Annotated[str, Depends(verificar_credenciales)],
):
    """Elimina una visita con sentido."""
    eliminar_visita(row_id)
    return RedirectResponse(url="/dashboard?tab=visitas", status_code=303)


@app.post("/dashboard/limpiar-visitas")
def limpiar_visitas_endpoint(
    _: Annotated[str, Depends(verificar_credenciales)],
):
    """Limpia TODOS los registros de Visitas con Sentido."""
    limpiar_visitas()
    return RedirectResponse(url="/dashboard?tab=visitas", status_code=303)


@app.post("/dashboard/limpiar-punto-compra")
def limpiar_punto_compra_endpoint(
    _: Annotated[str, Depends(verificar_credenciales)],
):
    """Limpia TODOS los registros de Punto de Compra."""
    limpiar_punto_compra()
    return RedirectResponse(url="/dashboard?tab=punto-compra", status_code=303)


@app.get("/dashboard/export")
def exportar_excel(
    _: Annotated[str, Depends(verificar_credenciales)],
):
    """Exporta visitas y punto de compra a Excel."""
    wb = openpyxl.Workbook()

    # Hoja 1: Visitas con Sentido
    ws1 = wb.active
    ws1.title = "Visitas con Sentido"
    headers1 = [
        "ID", "Fecha", "Usuario", "Local", "Geo Lat", "Geo Lng",
        "G. Saludó", "G. Preguntó",
        "P. Saludó", "P. Ofreció Ayuda",
        "Colaborador", "Resolutivo (1-5)", "Comentarios Sala",
        "Tiempo Fila", "Cajero Tipo",
        "Q9", "Q10 PMC", "Q11 Líder BCI", "Q12 Boleta Mail", "Q13 Despedida",
        "Comentarios Pago", "Comentarios Adicionales",
    ]
    ws1.append(headers1)
    for r in obtener_todas_visitas():
        ws1.append([
            r["id"], r["fecha"], r["usuario"], r["local"],
            r.get("geo_lat", ""), r.get("geo_lng", ""),
            r.get("q4a", ""), r.get("q4b", ""),
            r.get("q5a", ""), r.get("q5b", ""),
            r.get("q6", ""), r.get("q8_resolutivo", ""), r.get("comentarios_sala", ""),
            r.get("tiempo_fila", ""), r.get("q8_cajero_tipo", ""),
            r.get("q9", ""), r.get("q10", ""), r.get("q11", ""),
            r.get("q12", ""), r.get("q13", ""),
            r.get("comentarios_pago", ""), r.get("q17", ""),
        ])

    # Hoja 2: Entrevistas de Visitas
    ws2 = wb.create_sheet(title="Entrevistas Visitas")
    headers2 = [
        "Visita ID", "Usuario", "Local", "# Cliente",
        "Motivo Visita", "Aspectos Positivos", "Oportunidades Mejora",
    ]
    ws2.append(headers2)
    for r in obtener_todas_visitas():
        for e in obtener_entrevistas_visita(r["id"]):
            ws2.append([
                r["id"], r["usuario"], r["local"],
                e["numero_cliente"],
                e.get("motivo_visita", ""),
                e.get("aspectos_positivos", ""),
                e.get("oportunidades_mejora", ""),
            ])

    # Hoja 3: Punto de Compra
    ws3 = wb.create_sheet(title="Punto de Compra")
    headers3 = [
        "ID", "Fecha", "Nombre", "Tienda",
        "S1 Encontrar Sector", "S1 Exhibición", "S1 Obs",
        "S2 Vitrinear", "S2 Info Precio", "S2 Obs",
        "S3 Disponibilidad", "S3 Variedad", "S3 Obs",
        "S4 Pago", "S4 Tiempo", "S4 Obs",
    ]
    ws3.append(headers3)
    for r in obtener_todas_punto_compra():
        ws3.append([
            r["id"], r["fecha"], r["nombre"], r["tienda"],
            r.get("s1_i1", ""), r.get("s1_i2", ""), r.get("s1_obs", ""),
            r.get("s2_i1", ""), r.get("s2_i2", ""), r.get("s2_obs", ""),
            r.get("s3_i1", ""), r.get("s3_i2", ""), r.get("s3_obs", ""),
            r.get("s4_i1", ""), r.get("s4_i2", ""), r.get("s4_obs", ""),
        ])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=visitas_export.xlsx"},
    )

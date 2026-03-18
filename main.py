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
    eliminar_respuesta,
    init_db,
    insertar_entrevistas,
    insertar_respuesta,
    obtener_entrevistas,
    obtener_stats,
    obtener_todas,
    insertar_punto_compra,
    obtener_todas_punto_compra,
    eliminar_punto_compra,
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


# --- Formulario publico ---
@app.get("/", response_class=HTMLResponse)
def mostrar_formulario(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit")
def recibir_respuesta(
    formato: Annotated[str, Form()] = "",
    local: Annotated[str, Form()] = "",
    usuario: Annotated[str, Form()] = "",
    q4: Annotated[str, Form()] = "",
    q5: Annotated[str, Form()] = "",
    q6: Annotated[str, Form()] = "",
    q7: Annotated[str, Form()] = "",
    q8: Annotated[str, Form()] = "",
    q9: Annotated[str, Form()] = "",
    q10: Annotated[str, Form()] = "",
    q11: Annotated[str, Form()] = "",
    q12: Annotated[str, Form()] = "",
    q13: Annotated[str, Form()] = "",
    q17: Annotated[str, Form()] = "",
    # Entrevistas a clientes (JSON array)
    entrevistas_json: Annotated[str, Form()] = "[]",
):
    """Recibe el formulario completo con entrevistas a clientes."""
    # Insertar respuesta principal
    respuesta_id = insertar_respuesta({
        "formato": formato,
        "local": local,
        "usuario": usuario,
        "q4_guardia_saludo": q4,
        "q5_pasillos_saludo": q5,
        "q6_colaborador_resolutivo": q6,
        "q7_atencion_amable": q7,
        "q8_cajero_tipo": q8,
        "q9_cajero_saludo": q9,
        "q10_pmc": q10,
        "q11_lider_bci": q11,
        "q12_boleta_mail": q12,
        "q13_despedida": q13,
        "q17_comentarios": q17,
    })
    
    # Insertar entrevistas a clientes
    try:
        entrevistas = json.loads(entrevistas_json)
        if isinstance(entrevistas, list):
            insertar_entrevistas(respuesta_id, entrevistas)
    except json.JSONDecodeError:
        pass  # Si falla el JSON, continuar sin entrevistas
    
    return RedirectResponse(url="/gracias", status_code=303)


@app.get("/gracias", response_class=HTMLResponse)
def gracias(request: Request):
    return templates.TemplateResponse("gracias.html", {"request": request})


@app.get("/csat-seguridad", response_class=HTMLResponse)
def csat_seguridad(request: Request):
    """Reporte CSAT Seguridad YTD 2026."""
    return templates.TemplateResponse("csat_seguridad.html", {"request": request})


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


# --- Dashboard (protegido) ---
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    _: Annotated[str, Depends(verificar_credenciales)],
    formato: str = "",
    tab: str = "auditoria",
):
    rows = obtener_todas()
    if formato:
        rows = [r for r in rows if r["formato"] == formato]
    
    # Agregar entrevistas a cada row
    rows_con_entrevistas = []
    for row in rows:
        entrevistas = obtener_entrevistas(row["id"])
        rows_con_entrevistas.append({**row, "entrevistas": entrevistas})
    
    # Obtener datos de punto de compra
    punto_compra_rows = obtener_todas_punto_compra()
    
    stats = obtener_stats()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "rows": rows_con_entrevistas,
            "punto_compra_rows": punto_compra_rows,
            "stats": stats,
            "filtro": formato,
            "tab": tab,
        },
    )


@app.post("/dashboard/delete/{row_id}")
def eliminar(
    row_id: int,
    _: Annotated[str, Depends(verificar_credenciales)],
):
    """Elimina una respuesta por ID y redirige al dashboard."""
    eliminar_respuesta(row_id)
    return RedirectResponse(url="/dashboard", status_code=303)


@app.post("/dashboard/delete-punto-compra/{row_id}")
def eliminar_pc(
    row_id: int,
    _: Annotated[str, Depends(verificar_credenciales)],
):
    """Elimina una evaluación de punto de compra."""
    eliminar_punto_compra(row_id)
    return RedirectResponse(url="/dashboard?tab=punto-compra", status_code=303)


@app.get("/dashboard/export")
def exportar_excel(
    _: Annotated[str, Depends(verificar_credenciales)],
    formato: str = "",
):
    """Exporta las respuestas y entrevistas a Excel."""
    rows = obtener_todas()
    if formato:
        rows = [r for r in rows if r["formato"] == formato]

    wb = openpyxl.Workbook()
    
    # Hoja 1: Respuestas principales
    ws1 = wb.active
    ws1.title = "Respuestas"
    headers1 = [
        "ID", "Fecha", "Formato", "Local", "Usuario",
        "Guardia Saludo", "Pasillos Saludo", "Colaborador Resolutivo",
        "Atencion Amable", "Cajero Tipo", "Cajero Saludo",
        "PMC", "Lider BCI", "Boleta Mail", "Despedida", "Comentarios",
    ]
    ws1.append(headers1)
    for r in rows:
        ws1.append([
            r["id"], r["fecha"], r["formato"], r["local"], r["usuario"],
            r["q4_guardia_saludo"], r["q5_pasillos_saludo"], r["q6_colaborador_resolutivo"],
            r["q7_atencion_amable"], r["q8_cajero_tipo"], r["q9_cajero_saludo"],
            r["q10_pmc"], r["q11_lider_bci"], r["q12_boleta_mail"], r["q13_despedida"],
            r.get("q17_comentarios", ""),
        ])
    
    # Hoja 2: Entrevistas a clientes
    ws2 = wb.create_sheet(title="Entrevistas Clientes")
    headers2 = [
        "Respuesta ID", "Formato", "Local", "# Cliente",
        "Motivo Visita", "Aspectos Positivos", "Oportunidades Mejora",
    ]
    ws2.append(headers2)
    for r in rows:
        entrevistas = obtener_entrevistas(r["id"])
        for e in entrevistas:
            ws2.append([
                r["id"], r["formato"], r["local"], e["numero_cliente"],
                e["q14_motivo_visita"], e["q15_aspectos_positivos"], e["q16_oportunidades_mejora"],
            ])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=auditoria.xlsx"},
    )

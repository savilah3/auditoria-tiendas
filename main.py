import io
import os
import secrets
from typing import Annotated

import openpyxl
from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from database import eliminar_respuesta, init_db, insertar_respuesta, obtener_stats, obtener_todas

app = FastAPI(title="En los zapatos del cliente")
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

# ─── Credenciales del dashboard ──────────────────────────────────────────────
# Se leen desde variables de entorno (configúralas en Render)
DASHBOARD_USER = os.getenv("DASHBOARD_USER", "admin")
DASHBOARD_PASS = os.getenv("DASHBOARD_PASS", "walmart2025")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# ─── Autenticación básica para el dashboard ──────────────────────────────────
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


# ─── Formulario público ───────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def mostrar_formulario(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit")
def recibir_respuesta(
    formato: Annotated[str, Form()] = "",
    local: Annotated[str, Form()] = "",
    rut: Annotated[str, Form()] = "",
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
    q14: Annotated[str, Form()] = "",
):
    insertar_respuesta({
        "formato": formato,
        "local": local,
        "rut": rut,
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
        "q14_comentarios": q14,
    })
    return RedirectResponse(url="/gracias", status_code=303)


@app.get("/gracias", response_class=HTMLResponse)
def gracias(request: Request):
    return templates.TemplateResponse("gracias.html", {"request": request})


# ─── Dashboard (protegido) ────────────────────────────────────────────────────
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    _: Annotated[str, Depends(verificar_credenciales)],
    formato: str = "",
):
    rows = obtener_todas()
    if formato:
        rows = [r for r in rows if r["formato"] == formato]
    stats = obtener_stats()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "rows": rows, "stats": stats, "filtro": formato},
    )


@app.post("/dashboard/delete/{row_id}")
def eliminar(
    row_id: int,
    _: Annotated[str, Depends(verificar_credenciales)],
):
    """Elimina una respuesta por ID y redirige al dashboard."""
    eliminar_respuesta(row_id)
    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/dashboard/export")
def exportar_excel(
    _: Annotated[str, Depends(verificar_credenciales)],
    formato: str = "",
):
    rows = obtener_todas()
    if formato:
        rows = [r for r in rows if r["formato"] == formato]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Respuestas"

    headers = [
        "ID", "Fecha", "Formato", "Local", "RUT",
        "Guardia Saludo", "Pasillos Saludo", "Colaborador Resolutivo",
        "Atención Amable", "Cajero Tipo", "Cajero Saludo",
        "PMC", "Lider BCI", "Boleta Mail", "Despedida", "Comentarios",
    ]
    ws.append(headers)
    for r in rows:
        ws.append(list(r))

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=auditoria.xlsx"},
    )

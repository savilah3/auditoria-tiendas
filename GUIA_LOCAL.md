# 🚀 GUÍA: Auditoría Tiendas LOCAL + Cloudflare Tunnel

## ✅ PASO 1: Correr Servidor Local

### Opción A: Doble click en el archivo
```
INICIAR_LOCAL.bat
```

### Opción B: Desde terminal
```bash
cd auditoria_tiendas
python main_local.py
```

**Deberías ver:**
```
[+] Base de datos SQLite creada: auditoria_local.db
[+] Servidor LOCAL corriendo con SQLite
INFO:     Uvicorn running on http://0.0.0.0:8002
```

✅ **Tu app está corriendo en:** http://localhost:8002

---

## ✅ PASO 2: Instalar Cloudflare Tunnel

### Windows:

1. **Descargar cloudflared.exe**
   - Ve a: https://github.com/cloudflare/cloudflared/releases
   - Descarga: `cloudflared-windows-amd64.exe`
   - Renómbralo a: `cloudflared.exe`
   - Ponlo en: `C:\Windows\System32\` (o en la carpeta auditoria_tiendas)

2. **Verificar instalación**
```bash
cloudflared --version
```

---

## ✅ PASO 3: Crear Túnel Público

### En una NUEVA terminal:

```bash
cloudflared tunnel --url http://localhost:8002
```

**Deberías ver algo como:**
```
INFo[0000] Tunnel URL: https://abc-123-xyz.trycloudflare.com
```

✅ **¡Esa es tu URL PÚBLICA!** Compártela con tu equipo.

---

## 🎯 USO DIARIO:

### Terminal 1: Servidor Local
```bash
cd auditoria_tiendas
python main_local.py
```
(O doble click en `INICIAR_LOCAL.bat`)

### Terminal 2: Cloudflare Tunnel
```bash
cloudflared tunnel --url http://localhost:8002
```

**¡Listo!** Tu equipo puede acceder desde cualquier lugar con la URL de Cloudflare.

---

## 📊 ACCESO A LA APP:

### Formularios (públicos):
- **Visitas con Sentido**: https://tu-url.trycloudflare.com/visitas
- **Punto de Compra**: https://tu-url.trycloudflare.com/punto-compra

### Dashboard (requiere login):
- **URL**: https://tu-url.trycloudflare.com/dashboard
- **Usuario**: `admin`
- **Password**: `walmart2025`

---

## 💾 BASE DE DATOS:

Todo se guarda en: **auditoria_local.db**

### Backup manual:
```bash
# Copiar archivo
copy auditoria_local.db auditoria_backup_2026-04-07.db
```

### Ver datos (opcional):
Descarga **DB Browser for SQLite**: https://sqlitebrowser.org/

---

## ⚠️ NOTAS IMPORTANTES:

### ✅ Ventajas:
- **GRATIS FOREVER**
- **MUY RÁPIDO** (local)
- **Sin límites de uso**
- **Control total**

### ❌ Requisitos:
- **Tu PC debe estar PRENDIDA** mientras alguien use la app
- **Cloudflare Tunnel debe estar corriendo**
- La URL de Cloudflare **cambia cada vez** que reinicias el túnel

### 🔒 Seguridad:
- Cloudflare Tunnel es seguro (HTTPS automático)
- Dashboard protegido con usuario/password
- Formularios públicos (como debe ser para auditorías)

---

## 🆘 TROUBLESHOOTING:

### "Puerto 8002 ya en uso"
```bash
# Cambiar puerto en main_local.py línea final:
uvicorn.run(app, host="0.0.0.0", port=8003)  # Cambiar a 8003
```

### "cloudflared no reconocido"
- Verifica que `cloudflared.exe` esté en System32
- O corre desde la carpeta donde está el .exe

### "No puedo acceder desde otro PC"
- Verifica que ambas terminales estén corriendo
- Usa la URL de **Cloudflare**, NO localhost

### "Se perdieron mis datos"
- Verifica que `auditoria_local.db` exista
- Haz backup del archivo .db regularmente

---

## 📱 COMPARTIR CON TU EQUIPO:

**Envía este mensaje:**

```
Hola equipo 👋

Ya tenemos el checklist de auditorías disponible:

📋 Formulario Visitas: https://[tu-url].trycloudflare.com/visitas
🛒 Formulario Punto Compra: https://[tu-url].trycloudflare.com/punto-compra

Llénenlo desde su celular o PC. Los datos se guardan automáticamente.

¿Necesitan ver resultados? Pidan acceso al dashboard.

¡Gracias!
```

---

## 🎯 SIGUIENTE NIVEL (opcional):

### Túnel permanente con URL fija:
1. Crea cuenta Cloudflare (gratis)
2. Sigue guía: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/
3. Obtendrás URL permanente tipo: `auditoria.tudominio.com`

---

**¿Preguntas? Avísame y te ayudo! 🐶**

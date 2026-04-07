# 🚀 AUDITORÍA TIENDAS - LOCAL + CLOUDFLARE TUNNEL

## ✅ CONFIGURACIÓN COMPLETA (Solo una vez)

### PASO 1: Instalar Cloudflare Tunnel

Doble click en:
```
INSTALAR_CLOUDFLARE.bat
```

Esto descarga `cloudflared.exe` automáticamente.

---

## 🎯 USO DIARIO (2 pasos cada vez)

### PASO 1: Iniciar Servidor Local

**Terminal 1** - Doble click en:
```
INICIAR_LOCAL.bat
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8002
```

✅ **Servidor LOCAL funcionando**

---

### PASO 2: Crear Túnel Público

**Terminal 2** (NUEVA ventana) - Doble click en:
```
CREAR_TUNEL.bat
```

Busca la línea que dice:
```
https://abc-123-xyz.trycloudflare.com
```

✅ **Esa es tu URL PÚBLICA** - Compártela con tu equipo

---

## 📱 ACCESO A LA APP

### Formularios (PÚBLICOS):
- **Visitas con Sentido**: `https://tu-url.trycloudflare.com/visitas`
- **Punto de Compra**: `https://tu-url.trycloudflare.com/punto-compra`

### Dashboard (PROTEGIDO):
- **URL**: `https://tu-url.trycloudflare.com/dashboard`
- **Usuario**: `admin`
- **Password**: `walmart2025`

---

## 💾 BASE DE DATOS

Todo se guarda en:
```
auditoria_local.db
```

### Hacer Backup:
1. Cierra el servidor
2. Copia el archivo `auditoria_local.db` a otro lugar
3. Listo

---

## 🔧 CONFIGURACIÓN AVANZADA

### Cambiar usuario/password del dashboard:

Edita `.env` (o crea el archivo):
```
DASHBOARD_USER=tu_usuario
DASHBOARD_PASS=tu_password_seguro
```

### Cambiar puerto del servidor:

Edita `main_local.py` línea final:
```python
uvicorn.run(app, host="0.0.0.0", port=8003)  # Cambiar 8002 → 8003
```

Luego en `CREAR_TUNEL.bat` cambia:
```
--url http://localhost:8003
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### "Puerto 8002 ya en uso"
```bash
# Ver qué está usando el puerto
netstat -ano | findstr :8002

# Matar el proceso (reemplaza PID)
taskkill /F /PID <numero_pid>
```

### "No puedo acceder desde mi celular"
- ✅ USA la URL de **Cloudflare** (`https://xyz.trycloudflare.com`)
- ❌ NO uses `http://localhost:8002` (solo funciona en tu PC)

### "La URL cambió"
- Es normal: Cloudflare cambia la URL cada vez que reinicias el túnel
- **Solución**: Deja el túnel corriendo todo el día
- **O**: Usa túnel permanente (ver guía avanzada en GUIA_LOCAL.md)

### "Se perdieron los datos"
- Verifica que `auditoria_local.db` exista
- Si lo borraste, se creará uno nuevo (vacío)
- **BACKUP**: Copia el .db regularmente

---

## 📊 EXPORTAR DATOS

1. Ve al Dashboard: `https://tu-url.trycloudflare.com/dashboard`
2. Login con `admin` / `walmart2025`
3. Click en **"Exportar a Excel"**
4. Se descarga `visitas_export.xlsx` con 3 hojas:
   - Visitas con Sentido
   - Entrevistas
   - Punto de Compra

---

## ✅ VENTAJAS DE ESTA SOLUCIÓN

| Feature | Estado |
|---------|--------|
| Costo | ✅ GRATIS FOREVER |
| Velocidad | ✅ Ultra rápido (local) |
| Límites de uso | ✅ Sin límites |
| SSL/HTTPS | ✅ Automático (Cloudflare) |
| Acceso público | ✅ Desde cualquier lugar |
| Control total | ✅ 100% en tu PC |

## ⚠️ REQUISITOS

- ✅ Tu PC debe estar **PRENDIDA** mientras alguien use la app
- ✅ Ambas terminales deben estar **CORRIENDO**
- ✅ Debes estar conectado a **VPN/Eagle WiFi** de Walmart

---

## 📞 SOPORTE

¿Problemas? Lee:
- `GUIA_LOCAL.md` - Guía completa
- `README.md` - Este archivo

---

**¡Todo listo! Ahora tu checklist funciona 100% gratis, para siempre 🎉**

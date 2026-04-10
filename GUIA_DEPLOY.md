# GUÍA RÁPIDA: DEPLOY DEL NUEVO FORMULARIO VISITAS V2

## ✅ ¿QUÉ SE ACTUALIZÓ?

El formulario de "Visitas con Sentido" ahora tiene:
- ✅ Nuevos campos de atención (Guardia, Pasillos, Colaborador, CSAT)
- ✅ Botón "Enviando..." que previene errores si tarda
- ✅ Geolocalización automática
- ✅ Migración automática de BD (no pierdes datos existentes)

---

## 🚀 PASOS PARA PUBLICAR (3 OPCIONES)

### OPCIÓN 1: AUTOMÁTICA (Recomendada)

1. **Doble clic en `COMMIT_Y_PUSH.bat`**
2. Revisar archivos que se commitearán
3. Presionar Enter para confirmar
4. Escribir `S` y Enter para hacer push
5. Ir a https://dashboard.render.com
6. Verificar que el deploy automático inició
7. Esperar ~2-3 minutos
8. ✅ LISTO! Probar en tu URL de Render

---

### OPCIÓN 2: MANUAL (Si prefieres control total)

```bash
# En terminal/cmd:
cd "C:\Users\savila3\Documents\puppy_workspace\auditoria_tiendas"

# Ver cambios
git status

# Agregar archivos
git add templates/visitas.html database.py main.py RESUMEN_ACTUALIZACION_V2.txt

# Commit
git commit -m "Actualizar formulario Visitas con Sentido v2"

# Push
git push origin main
```

Luego ir a Render → Tu servicio → Verificar deploy automático

---

### OPCIÓN 3: PROBAR PRIMERO (Más seguro)

1. **Doble clic en `PROBAR_LOCAL.bat`**
2. Esperar a que se inicie el servidor
3. Abrir http://localhost:8000/visitas
4. Probar el formulario completo
5. Verificar que funcione todo
6. Presionar Ctrl+C para detener servidor
7. Si todo OK → Usar OPCIÓN 1 o 2

---

## 🔍 VERIFICAR QUE FUNCIONA

### 1. En el formulario (/visitas):
- [ ] Carga correctamente
- [ ] "📍 Ubicación capturada" aparece arriba
- [ ] Puedes seleccionar usuario
- [ ] Puedes seleccionar local
- [ ] Todos los checkboxes/radios funcionan
- [ ] Botón "Finalizar y Enviar" muestra "⏳ Enviando..."
- [ ] Redirige a página de gracias

### 2. En el dashboard (/dashboard):
- [ ] Ingresar con usuario: admin / contraseña: walmart2025
- [ ] Ver tab "Visitas con Sentido"
- [ ] Ver tu visita de prueba
- [ ] Descargar Excel → Verificar que incluye nuevas columnas

---

## ⚠️ SI ALGO FALLA

### Error: "Column 'q3' does not exist"
**Solución:** La migración automática se ejecuta al iniciar. Reinicia el servicio en Render.

### Error: "Enviando..." no aparece
**Solución:** Hacer Ctrl+F5 en el navegador para refrescar cache.

### Error: Timeout al enviar formulario
**Solución:** Normal si la BD está lejos. El timeout es de 30 segundos y muestra mensaje al usuario.

### Rollback (volver atrás)
```bash
# Ver commits anteriores
git log --oneline

# Volver al commit anterior
git revert HEAD
git push origin main
```

O en Render:
- Manual Deploy → Rollback to [commit anterior]

---

## 📝 ARCHIVOS IMPORTANTES

| Archivo | Descripción |
|---------|-------------|
| `templates/visitas.html` | Nuevo formulario (reemplazado) |
| `database.py` | Nuevos campos + migración automática |
| `main.py` | Endpoint actualizado |
| `RESUMEN_ACTUALIZACION_V2.txt` | Resumen técnico completo |
| `COMMIT_Y_PUSH.bat` | Script para publicar |
| `PROBAR_LOCAL.bat` | Script para probar localmente |

---

## ✨ MEJORAS INCLUIDAS

### Para los usuarios:
- ✅ Mensaje "Enviando..." al presionar botón
- ✅ No se puede hacer doble-submit
- ✅ Geolocalización automática
- ✅ Mejor UX en campos "Otro" (se muestran/ocultan automáticamente)

### Para ti (admin):
- ✅ Excel con todas las nuevas columnas
- ✅ Migración automática (no pierdes datos viejos)
- ✅ Nuevos campos aparecen en dashboard

---

## 🆘 NECESITAS AYUDA?

1. Revisar `RESUMEN_ACTUALIZACION_V2.txt` (más detallado)
2. Revisar logs en Render → Tu servicio → Logs
3. Contactar a Code Puppy 🐶

---

**¡Listo para publicar! 🚀**

La forma más rápida es hacer doble clic en `COMMIT_Y_PUSH.bat` y listo.

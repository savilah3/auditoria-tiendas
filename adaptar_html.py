"""Script para adaptar el nuevo HTML de Visitas con Sentido."""
import re

# Leer el nuevo HTML descargado
with open(r"C:\Users\savila3\Downloads\Visitas con Sentido-F.Atencion.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Cambiar la action del formulario
html = html.replace(
    'action="AQUI_VA_TU_URL_DE_DESTINO"',
    'action="/submit-visita" onsubmit="return enviarFormulario(event)"'
)

# 2. Buscar dónde termina el último <script> antes de </head>
# y agregar la función de envío y geolocalización

script_envio = '''
    <script>
        // Enviar formulario con fetch y manejo de errores
        async function enviarFormulario(event) {
            event.preventDefault();
            
            const submitBtn = document.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Mostrar loading
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="animate-pulse">⏳ Enviando... Por favor espera</span>';
            
            try {
                const form = document.getElementById('evaluationForm');
                const formData = new FormData(form);
                
                // Timeout de 30 segundos
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 30000);
                
                const response = await fetch('/submit-visita', {
                    method: 'POST',
                    body: formData,
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (response.redirected) {
                    window.location.href = response.url;
                } else if (response.ok) {
                    window.location.href = '/gracias';
                } else {
                    throw new Error('Error del servidor: ' + response.status);
                }
            } catch (error) {
                console.error('Error:', error);
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
                
                if (error.name === 'AbortError') {
                    alert('La conexión tardó demasiado. Por favor verifica tu conexión e intenta de nuevo.');
                } else {
                    alert('Error al enviar: ' + error.message + '\\n\\nPor favor intenta de nuevo.');
                }
            }
            
            return false;
        }

        // Geolocation Logic
        window.addEventListener('load', () => {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        document.getElementById('geo_lat').value = position.coords.latitude;
                        document.getElementById('geo_lng').value = position.coords.longitude;
                        document.getElementById('geo_status').innerHTML = '📍 Ubicación capturada';
                        document.getElementById('geo_status').classList.replace('text-gray-400', 'text-green-600');
                    },
                    (error) => {
                        console.warn("Geolocalización no permitida o no disponible.", error);
                        document.getElementById('geo_status').innerHTML = '📍 Ubicación no disponible';
                    },
                    { enableHighAccuracy: true, timeout: 10000 }
                );
            }
        });
    </script>
'''

# Insertar antes de </head>
html = html.replace('</head>', script_envio + '\n</head>')

# 3. Actualizar el name del campo usuario para que coincida con el backend
html = html.replace('name="q1"', 'name="usuario"')
html = html.replace('id="q1"', 'id="usuario"')

# 4. Actualizar el name del campo local
html = html.replace('name="q2_local"', 'name="local"')
html = html.replace('id="q2_local"', 'id="local"')

# 5. Actualizar el name del campo formato
html = html.replace('name="q2_formato"', 'name="formato"')
html = html.replace('id="q2_formato"', 'id="formato"')

# 6. Asegurarnos que el campo de comentarios finales está mapeado correctamente
# (ya está como q17 en el HTML nuevo, perfecto!)

# Guardar el archivo adaptado
output_path = r"C:\Users\savila3\Documents\puppy_workspace\auditoria_tiendas\templates\visitas.html"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print("HTML adaptado guardado en: {}".format(output_path))
print("\nCambios aplicados:")
print("  1. Action del formulario -> /submit-visita")
print("  2. Agregada funcion enviarFormulario() con loading")
print("  3. Agregada geolocalizacion automatica")
print("  4. Campos renombrados:")
print("     - q1 -> usuario")
print("     - q2_local -> local")
print("     - q2_formato -> formato")
print("\nSIGUIENTE PASO: Actualizar main.py para manejar los nuevos campos")

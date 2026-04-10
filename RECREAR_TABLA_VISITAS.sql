-- ═══════════════════════════════════════════════════════════════════
-- SCRIPT SQL PARA RECREAR TABLA VISITAS DESDE CERO
-- ═══════════════════════════════════════════════════════════════════
-- Ejecutar en: Render Dashboard → PostgreSQL → psql o Query
-- ═══════════════════════════════════════════════════════════════════

-- PASO 1: ELIMINAR tabla vieja (si existe)
DROP TABLE IF EXISTS visitas CASCADE;

-- PASO 2: CREAR tabla nueva con TODAS las columnas
CREATE TABLE visitas (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    geo_lat TEXT,
    geo_lng TEXT,
    usuario TEXT,
    local TEXT,
    
    -- Paso 1: Atención (campos nuevos)
    q3 TEXT,
    q3_otro_text TEXT,
    q4 TEXT,
    q4_otro_text TEXT,
    q5 TEXT,
    q5_otro_text TEXT,
    q6 TEXT,
    q6_otro_text TEXT,
    q7 TEXT,
    q7_otro_text TEXT,
    q8_csat TEXT,
    q9_new TEXT,
    q9_new_otro_text TEXT,
    
    -- Paso 2: Zona de pago
    q8 TEXT,
    q9 TEXT,
    q10 TEXT,
    q11 TEXT,
    q12 TEXT,
    q13 TEXT,
    
    -- Paso 3: Comentarios
    q17 TEXT
);

-- PASO 3: Verificar que se creó correctamente
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'visitas'
ORDER BY ordinal_position;

-- ═══════════════════════════════════════════════════════════════════
-- RESULTADO ESPERADO:
-- Deberías ver una lista con TODAS estas columnas:
--   id, fecha, geo_lat, geo_lng, usuario, local,
--   q3, q3_otro_text, q4, q4_otro_text, q5, q5_otro_text,
--   q6, q6_otro_text, q7, q7_otro_text, q8_csat, 
--   q9_new, q9_new_otro_text, q8, q9, q10, q11, q12, q13, q17
-- ═══════════════════════════════════════════════════════════════════

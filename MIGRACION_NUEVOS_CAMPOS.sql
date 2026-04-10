-- MIGRACIÓN: Nuevos campos para Visitas con Sentido v2
-- Ejecutar SOLO si se quiere actualizar la estructura de la tabla visitas

-- Opción 1: Agregar nuevos campos a la tabla existente (PRESERVA DATOS)
ALTER TABLE visitas ADD COLUMN IF NOT EXISTS q3 TEXT;
ALTER TABLE visitas ADD COLUMN IF NOT EXISTS q3_otro_text TEXT;
ALTER TABLE visitas ADD COLUMN IF NOT EXISTS q7 TEXT;
ALTER TABLE visitas ADD COLUMN IF NOT EXISTS q7_otro_text TEXT;
ALTER TABLE visitas ADD COLUMN IF NOT EXISTS q8_csat TEXT;
ALTER TABLE visitas ADD COLUMN IF NOT EXISTS q9_new TEXT;
ALTER TABLE visitas ADD COLUMN IF NOT EXISTS q9_new_otro_text TEXT;

-- Renombrar campos para claridad (OPCIONAL)
-- ALTER TABLE visitas RENAME COLUMN q4a TO q4;
-- ALTER TABLE visitas RENAME COLUMN q4a_other TO q4_otro_text;
-- ALTER TABLE visitas RENAME COLUMN q5a TO q5;
-- ALTER TABLE visitas RENAME COLUMN q5a_other TO q5_otro_text;
-- ALTER TABLE visitas RENAME COLUMN q6_other TO q6_otro_text;

-- Opción 2: Recrear tabla completa (BORRA TODOS LOS DATOS)
-- Solo descomentar si quieres empezar desde cero
/*
DROP TABLE IF EXISTS entrevistas_visitas CASCADE;
DROP TABLE IF EXISTS visitas CASCADE;

CREATE TABLE visitas (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    geo_lat TEXT,
    geo_lng TEXT,
    usuario TEXT,
    local TEXT,
    -- Paso 1: Atención
    q3 TEXT, q3_otro_text TEXT,           -- Guardia saludo
    q4 TEXT, q4_otro_text TEXT,           -- Guardia pregunto si necesitas algo
    q5 TEXT, q5_otro_text TEXT,           -- Pasillos saludo
    q6 TEXT, q6_otro_text TEXT,           -- Pasillos preguntaron si necesitas algo
    q7 TEXT, q7_otro_text TEXT,           -- Encontraste colaborador
    q8_csat TEXT,                         -- Satisfacción resolutividad (1-7)
    q9_new TEXT, q9_new_otro_text TEXT,   -- Te sentiste bienvenido
    -- Paso 2: Zona de pago
    q8 TEXT,                              -- Tipo cajero (interno/externo)
    q9 TEXT,                              -- Cajero saludo
    q10 TEXT,                             -- PMC
    q11 TEXT,                             -- Lider BCI
    q12 TEXT,                             -- Boleta mail
    q13 TEXT,                              -- Despedida
    -- Paso 3: Comentarios
    q17 TEXT                              -- Comentarios finales
);

CREATE TABLE entrevistas_visitas (
    id SERIAL PRIMARY KEY,
    visita_id INTEGER NOT NULL REFERENCES visitas(id) ON DELETE CASCADE,
    numero_cliente INTEGER NOT NULL,
    motivo_visita TEXT,
    aspectos_positivos TEXT,
    oportunidades_mejora TEXT
);
*/

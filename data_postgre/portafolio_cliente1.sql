WITH total_macroactivo AS (
    SELECT 
        id_sistema_cliente,
        macroactivo,
        SUM(CAST(aba AS numeric)) AS total_aba_macroactivo
    FROM 
        historico_aba_macroactivos
    WHERE 
        (ingestion_year, ingestion_month, ingestion_day) <= (
            SELECT MAX(ingestion_year), MAX(ingestion_month), MAX(ingestion_day)
            FROM historico_aba_macroactivos
        )
    GROUP BY 
        id_sistema_cliente, macroactivo
),
macroactivo_con_porcentaje AS (
    SELECT 
        id_sistema_cliente,
        macroactivo,
        total_aba_macroactivo,
        ROUND((total_aba_macroactivo / SUM(total_aba_macroactivo) OVER (PARTITION BY id_sistema_cliente)) * 100, 2) AS porcentaje_macroactivo
    FROM 
        total_macroactivo
),
porcentaje_por_macroactivo AS (
    SELECT 
        h.id_sistema_cliente,
        h.macroactivo,
        h.cod_activo,
        SUM(CAST(h.aba AS numeric)) AS total_aba_activo,
        ROUND((SUM(CAST(h.aba AS numeric)) / m.total_aba_macroactivo) * 100, 2) AS porcentaje_activo_macroactivo
    FROM 
        historico_aba_macroactivos h
    JOIN 
        total_macroactivo m ON h.id_sistema_cliente = m.id_sistema_cliente AND h.macroactivo = m.macroactivo
    GROUP BY 
        h.id_sistema_cliente, h.macroactivo, h.cod_activo, m.total_aba_macroactivo
),
resultado_final AS (
    SELECT
        pm.id_sistema_cliente,
        pm.macroactivo,
        c.activo AS nombre_activo,
        pm.total_aba_activo,
        pm.porcentaje_activo_macroactivo,
        mp.porcentaje_macroactivo
    FROM 
        porcentaje_por_macroactivo pm
    JOIN 
        catalogo_activos c ON pm.cod_activo = c.cod_activo
    JOIN 
        macroactivo_con_porcentaje mp ON pm.id_sistema_cliente = mp.id_sistema_cliente AND pm.macroactivo = mp.macroactivo
)
SELECT * FROM resultado_final
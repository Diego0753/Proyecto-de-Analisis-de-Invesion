SELECT 
    b.banca,
    h.macroactivo,
    SUM(CAST(h.aba AS numeric)) AS total_aba,
    (SUM(CAST(h.aba AS numeric)) / SUM(SUM(CAST(h.aba AS numeric))) OVER (PARTITION BY h.cod_banca)) * 100 AS porcentaje_macroactivo
FROM 
    historico_aba_macroactivos h
JOIN 
    catalogo_banca b ON h.cod_banca = b.cod_banca
WHERE 
    h.ingestion_year >= (SELECT MIN(ingestion_year) FROM historico_aba_macroactivos) AND
    h.ingestion_year <= (SELECT MAX(ingestion_year) FROM historico_aba_macroactivos)
GROUP BY 
    b.banca, h.macroactivo, h.cod_banca

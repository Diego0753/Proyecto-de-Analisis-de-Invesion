SELECT 
    TO_CHAR(TO_DATE(h.ingestion_year || '-' || h.ingestion_month || '-01', 'YYYY-MM-DD'), 'YYYY-MM') AS mes,
    ROUND(AVG(CAST(h.aba AS numeric)), 2) AS promedio_aba
FROM 
    historico_aba_macroactivos h
WHERE 
    h.ingestion_year >= (SELECT MIN(ingestion_year) FROM historico_aba_macroactivos) 
    AND h.ingestion_year <= (SELECT MAX(ingestion_year) FROM historico_aba_macroactivos)
GROUP BY 
    mes
ORDER BY 
    mes desc;


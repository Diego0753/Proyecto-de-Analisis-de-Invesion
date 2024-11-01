SELECT p.perfil_riesgo, 
       h.macroactivo, 
       SUM(CAST(h.aba AS numeric)) AS total_aba,
       ROUND((SUM(CAST(h.aba AS numeric)) / 
              SUM(SUM(CAST(h.aba AS numeric))) OVER (PARTITION BY h.cod_perfil_riesgo)) * 100, 2) AS porcentaje_macroactivo
FROM historico_aba_macroactivos h
JOIN cat_perfil_riesgo p ON h.cod_perfil_riesgo = p.cod_perfil_riesgo
WHERE h.ingestion_year >= (SELECT MIN(ingestion_year) FROM historico_aba_macroactivos) 
  AND h.ingestion_year <= (SELECT MAX(ingestion_year) FROM historico_aba_macroactivos)
GROUP BY p.perfil_riesgo, h.macroactivo, h.cod_perfil_riesgo

--12. Como variaram os obitos ao longo dos anos?

SELECT SUBSTRING(ESTATISTICAS.periodo,1,4) AS ano, SUM(ESTATISTICAS.obitos) AS obitos
FROM ESTATISTICAS
GROUP BY ano
ORDER BY ano;
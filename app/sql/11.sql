--11. Como variou o numero de obidos ao longo do tempo? Mostra o periodo e o numero de obidos. Ordena pelo crescente.

SELECT ESTATISTICAS.periodo, SUM(ESTATISTICAS.obitos) AS obidos
FROM ESTATISTICAS
GROUP BY ESTATISTICAS.periodo
ORDER BY periodo

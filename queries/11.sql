--11. Como variou o número de óbidos ao longo do tempo? Mostra o periodo e o número de óbidos. Ordena pelo crescente.

SELECT ESTATISTICAS.periodo, SUM(ESTATISTICAS.obitos) AS obidos
FROM ESTATISTICAS
GROUP BY ESTATISTICAS.periodo
ORDER BY periodo
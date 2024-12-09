--7. Qual a percentagem de óbitos por doença? Mostra o id da doença, a descrição da doença e, dos registados (óbitos+internamentos+ambulatório), a percentagem de quantos foram óbitos. Ordena pela percentagem descendente.

SELECT DOENCAS.doenca_id as id, DOENCAS.descricao as doenca, AVG(ESTATISTICAS.obitos*1.0/(ESTATISTICAS.obitos+ESTATISTICAS.ambulatorio+ESTATISTICAS.internamentos))*100 AS percentagem
FROM ESTATISTICAS
NATURAL JOIN DOENCAS
WHERE (ESTATISTICAS.obitos+ESTATISTICAS.ambulatorio+ESTATISTICAS.internamentos)>0
GROUP BY DOENCAS.doenca_id
ORDER BY percentagem DESC
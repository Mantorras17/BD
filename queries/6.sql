--6. Qual é o número de óbitos por doença? Mostra o id da doença, a descrição da doença e o número de óbitos, ordenado pelo id da doença.

SELECT DOENCAS.doenca_id as id, DOENCAS.descricao as doenca, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN DOENCAS
GROUP BY DOENCAS.doenca_id
ORDER BY obitos DESC
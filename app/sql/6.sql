--6. Qual e o numero de obitos por doenca? Mostra o id da doenca, a descricao da doenca e o numero de obitos, ordenado pelo id da doenca.

SELECT DOENCAS.doenca_id as id, DOENCAS.descricao as doenca, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN DOENCAS
GROUP BY DOENCAS.doenca_id
ORDER BY obitos DESC

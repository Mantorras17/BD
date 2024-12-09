--9. Qual a média de dias de internamento, para cada doença? Mostra o id da doença, a descrição da doença, e a média de dias de internamento. Ordena por média descendente.

SELECT DOENCAS.doenca_id as id, DOENCAS.descricao as doenca, SUM(ESTATISTICAS.dias_de_internamento)/SUM(ESTATISTICAS.internamentos) AS media
FROM ESTATISTICAS
NATURAL JOIN DOENCAS
GROUP BY DOENCAS.doenca_id
ORDER BY media DESC
--9. Qual a media de dias de internamento, para cada doenca? Mostra o id da doenca, a descricao da doenca, e a media de dias de internamento. Ordena por media descendente.

SELECT DOENCAS.doenca_id as id, DOENCAS.descricao as doenca, SUM(ESTATISTICAS.dias_de_internamento)/SUM(ESTATISTICAS.internamentos) AS media
FROM ESTATISTICAS
NATURAL JOIN DOENCAS
GROUP BY DOENCAS.doenca_id
ORDER BY media DESC

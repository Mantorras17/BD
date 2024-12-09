--4. Qual é o número total de internamentos por hospital? Mostra o nome do hospital e o número de internamentos, ordenado pelo numero de internamentos descendente.

SELECT HOSPITAIS.hospital_id as id, HOSPITAIS.nome as hospital, SUM(ESTATISTICAS.internamentos) AS internamentos
FROM ESTATISTICAS
NATURAL JOIN HOSPITAIS
GROUP BY HOSPITAIS.hospital_id
ORDER BY internamentos DESC
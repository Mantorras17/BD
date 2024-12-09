--4. Qual e o numero total de internamentos por hospital? Mostra o nome do hospital e o numero de internamentos, ordenado pelo numero de internamentos descendente.

SELECT HOSPITAIS.hospital_id as id, HOSPITAIS.nome as hospital, SUM(ESTATISTICAS.internamentos) AS internamentos
FROM ESTATISTICAS
NATURAL JOIN HOSPITAIS
GROUP BY HOSPITAIS.hospital_id
ORDER BY internamentos DESC

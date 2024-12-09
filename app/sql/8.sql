--8. Qual a percentagem de óbitos por hospital? Mostra o código do hospital, o nome do hospital e, dos registados (óbitos+internamentos+ambulatório), a percentagem de quantos foram óbitos. Ordena pela percentagem descendente.

SELECT HOSPITAIS.hospital_id as id, HOSPITAIS.nome as hospital, AVG(ESTATISTICAS.obitos*1.0/(ESTATISTICAS.obitos+ESTATISTICAS.ambulatorio+ESTATISTICAS.internamentos))*100 AS percentagem
FROM ESTATISTICAS
NATURAL JOIN HOSPITAIS
WHERE (ESTATISTICAS.obitos+ESTATISTICAS.ambulatorio+ESTATISTICAS.internamentos)>0
GROUP BY HOSPITAIS.hospital_id
ORDER BY percentagem DESC
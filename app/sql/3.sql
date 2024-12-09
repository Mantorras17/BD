--3. Qual é o número de óbitos registados por região? Mostra o nome da região e o número de óbitos, ordenado pelo numero de óbitos descendente.

SELECT REGIOES.nome, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN HOSPITAIS
JOIN REGIOES ON HOSPITAIS.regiao_id = REGIOES.regiao_id
GROUP BY REGIOES.regiao_id
ORDER BY obitos DESC
--5. Quais as regiões com o número de óbitos maior que 10000? Mostra o nome da região, o número de óbidos e o número de óbitos. Ordenados pelo número de óbidos decrescente.

SELECT REGIOES.nome, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN HOSPITAIS
JOIN REGIOES ON HOSPITAIS.regiao_id = REGIOES.regiao_id
GROUP BY REGIOES.regiao_id
HAVING SUM(ESTATISTICAS.obitos)>10000
ORDER BY obitos DESC

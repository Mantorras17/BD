--5. Quais as regioes com o numero de obitos maior que 10000? Mostra o nome da regiao, o numero de obidos e o numero de obitos. Ordenados pelo numero de obitos decrescente.

SELECT REGIOES.nome, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN HOSPITAIS
JOIN REGIOES ON HOSPITAIS.regiao_id = REGIOES.regiao_id
GROUP BY REGIOES.regiao_id
HAVING SUM(ESTATISTICAS.obitos)>10000
ORDER BY obitos DESC

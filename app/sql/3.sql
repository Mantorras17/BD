--3. Qual e o numero de obitos registados por regiao? Mostra o nome da regiao e o numero de obitos, ordenado pelo numero de obitos descendente.

SELECT REGIOES.nome, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN HOSPITAIS
JOIN REGIOES ON HOSPITAIS.regiao_id = REGIOES.regiao_id
GROUP BY REGIOES.regiao_id
ORDER BY obitos DESC

--1. Qual é o número de óbitos por género? Mostra o género e o número de óbitos.

SELECT GRUPOS.genero, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN GRUPOS
GROUP BY GRUPOS.genero
ORDER BY obitos DESC
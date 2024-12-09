--1. Qual e o numero de obitos por genero? Mostra o genero e o numero de obitos.

SELECT GRUPOS.genero, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN GRUPOS
GROUP BY GRUPOS.genero
ORDER BY obitos DESC

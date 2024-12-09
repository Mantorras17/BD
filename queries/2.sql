--2. Qual é o número de óbitos por faixa etaria? Mostra a idade minima, idade máxima, e o número de óbitos. Ordena por idade mínima.

SELECT FAIXAS_ETARIAS.idade_min, FAIXAS_ETARIAS.idade_max, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN GRUPOS
JOIN FAIXAS_ETARIAS ON GRUPOS.faixa_etaria_id = FAIXAS_ETARIAS.faixa_etaria_id
GROUP BY FAIXAS_ETARIAS.idade_min
ORDER BY obitos DESC
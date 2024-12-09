--2. Qual e o numero de obitos por faixa etaria? Mostra a idade minima, idade maxima, e o numero de obitos. Ordena por idade minima.

SELECT FAIXAS_ETARIAS.idade_min, FAIXAS_ETARIAS.idade_max, SUM(ESTATISTICAS.obitos) as obitos
FROM ESTATISTICAS
NATURAL JOIN GRUPOS
JOIN FAIXAS_ETARIAS ON GRUPOS.faixa_etaria_id = FAIXAS_ETARIAS.faixa_etaria_id
GROUP BY FAIXAS_ETARIAS.idade_min
ORDER BY obitos DESC

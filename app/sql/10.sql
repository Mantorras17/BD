--10. Qual o numero de obitos de criancas, adolescentes, adultos e idosos? Mostra o numero de obitos por criancas(0<=idade_min<15), jovens(idade_min>=15,idade_max<=25), adultos(idade_min>=25, idade_max<=65) e idosos(idade_min<=65).

SELECT 
    CASE 
        WHEN FAIXAS_ETARIAS.idade_min >= 0 AND FAIXAS_ETARIAS.idade_max <= 15 THEN 'Crianças'
        WHEN FAIXAS_ETARIAS.idade_min >= 15 AND FAIXAS_ETARIAS.idade_max <= 25 THEN 'Jovens'
        WHEN FAIXAS_ETARIAS.idade_min >= 25 AND FAIXAS_ETARIAS.idade_max <= 65 THEN 'Adultos'
        WHEN FAIXAS_ETARIAS.idade_min >= 65 THEN 'Idosos'
    END AS faixa_etaria, SUM(ESTATISTICAS.obitos) AS obitos
FROM ESTATISTICAS
NATURAL JOIN GRUPOS
NATURAL JOIN FAIXAS_ETARIAS
GROUP BY faixa_etaria
ORDER BY obitos DESC

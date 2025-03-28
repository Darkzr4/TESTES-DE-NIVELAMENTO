SELECT 
    o.razao_social,
    o.registro_ans,
    SUM(d.vl_saldo_final) AS total_despesas_anual,
    COUNT(DISTINCT QUARTER(d.data)) AS trimestres_com_dados,
    MAX(d.data) AS data_mais_recente
FROM 
    demonstracoes_contabeis d
JOIN 
    operadoras o ON d.reg_ans = o.registro_ans
WHERE 
    (
        d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
        OR d.descricao LIKE '%EVENTOS%SINISTROS%ASSISTÊNCIA%SAÚDE%MEDICO%HOSPITALAR%'
        OR d.descricao = 'Despesas com Eventos / Sinistros'
    )
    AND d.data >= DATE_SUB('2024-10-01', INTERVAL 1 YEAR)
GROUP BY 
    o.razao_social, o.registro_ans
ORDER BY 
    total_despesas_anual DESC
LIMIT 10;
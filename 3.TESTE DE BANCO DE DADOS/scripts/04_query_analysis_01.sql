-- Query 1: 10 operadoras com maiores despesas no último trimestre
SELECT 
    o.razao_social,
    o.registro_ans,
    SUM(d.vl_saldo_final) AS total_despesas,
    MAX(d.data) AS data_ultimo_registro,
    COUNT(*) AS qtde_registros
FROM 
    demonstracoes_contabeis d
JOIN 
    operadoras o ON d.reg_ans = o.registro_ans
WHERE 
    (
        d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
        OR d.descricao LIKE '%EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE%'
        OR d.descricao LIKE '%EVENTOS%SINISTROS%ASSISTÊNCIA%SAÚDE%MEDICO%HOSPITALAR%'
    )
    AND d.data >= DATE_SUB('2024-10-01', INTERVAL 3 MONTH)
GROUP BY 
    o.razao_social, o.registro_ans
ORDER BY 
    total_despesas DESC
LIMIT 10;
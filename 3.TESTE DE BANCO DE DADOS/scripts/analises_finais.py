# Execução das queries 01 e 02 via python

import mysql.connector
from datetime import datetime

def executar_analises_finais():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'demonstracoes_contabeis_ans'
    }

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Obtém a data mais recente
        cursor.execute("SELECT MAX(data) AS data_max FROM demonstracoes_contabeis")
        data_mais_recente = cursor.fetchone()['data_max']

        print(f"\n=== ANÁLISES ATUALIZADAS (Base: {data_mais_recente}) ===\n")

        # Query 1: Último Trimestre
        print("\n=== TOP 10 OPERADORAS - MAIORES DESPESAS (ÚLTIMO TRIMESTRE) ===\n")
        query_trimestre = """
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
                d.descricao LIKE %s
                OR d.descricao LIKE %s
                OR d.descricao LIKE %s
            )
            AND d.data >= DATE_SUB(%s, INTERVAL 3 MONTH)
        GROUP BY 
            o.razao_social, o.registro_ans
        ORDER BY 
            total_despesas DESC
        LIMIT 10;
        """
        cursor.execute(query_trimestre, [
            '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%',
            '%EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE%',
            '%EVENTOS%SINISTROS%ASSISTÊNCIA%SAÚDE%MEDICO%HOSPITALAR%',
            data_mais_recente
        ])

        for i, row in enumerate(cursor.fetchall(), 1):
            print(f"{i}. {row['razao_social']} (ANS: {row['registro_ans']})")
            print(f"   Total Despesas: R$ {row['total_despesas']:,.2f}")
            print(f"   Registros: {row['qtde_registros']} | Último: {row['data_ultimo_registro']}\n")

        # Query 2: Último Ano
        print("\n=== TOP 10 OPERADORAS - MAIORES DESPESAS (ÚLTIMO ANO) ===\n")
        query_ano = """
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
                d.descricao LIKE %s
                OR d.descricao LIKE %s
                OR d.descricao = %s
            )
            AND d.data >= DATE_SUB(%s, INTERVAL 1 YEAR)
        GROUP BY 
            o.razao_social, o.registro_ans
        ORDER BY 
            total_despesas_anual DESC
        LIMIT 10;
        """
        cursor.execute(query_ano, [
            '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%',
            '%EVENTOS%SINISTROS%ASSISTÊNCIA%SAÚDE%MEDICO%HOSPITALAR%',
            'Despesas com Eventos / Sinistros',
            data_mais_recente
        ])

        for i, row in enumerate(cursor.fetchall(), 1):
            print(f"{i}. {row['razao_social']} (ANS: {row['registro_ans']})")
            print(f"   Total Anual: R$ {row['total_despesas_anual']:,.2f}")
            print(f"   Trimestres com dados: {row['trimestres_com_dados']}/4 | Último: {row['data_mais_recente']}\n")

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    executar_analises_finais()
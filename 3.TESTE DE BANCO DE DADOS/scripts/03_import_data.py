import mysql.connector
import csv
from tqdm import tqdm
from datetime import datetime

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'demonstracoes_contabeis_ans',
    'charset': 'utf8mb4'
}

def conectar_banco():
    """Estabelece conexão com o MySQL"""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def formatar_data(data_str):
    """Converte data no formato dd/mm/yyyy para objeto date, tratando casos especiais"""
    if not data_str or str(data_str).strip() in ('', 'NULL', 'None'):
        return None
    
    try:
        data_str = str(data_str).strip()
        if '-' in data_str and len(data_str) == 10:
            return datetime.strptime(data_str, '%Y-%m-%d').date()
        return datetime.strptime(data_str, '%d/%m/%Y').date()
    except Exception as e:
        print(f"Erro ao converter data '{data_str}': {e}")
        return None

def converter_data(data_str):
    """Converte data em formatos DD/MM/YYYY ou YYYY-MM-DD para objeto date"""
    if not data_str or str(data_str).strip() in ('', 'NULL', 'None'):
        return None
    
    data_str = str(data_str).strip().strip('"')
    
    try:
        if len(data_str) == 10 and data_str[2] == '/' and data_str[5] == '/':
            return datetime.strptime(data_str, '%d/%m/%Y').date()
        elif len(data_str) == 10 and data_str[4] == '-' and data_str[7] == '-':
            return datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError as e:
        print(f"Formato de data não reconhecido: '{data_str}' - {e}")
    
    return None

def limpar_tabelas(conn):
    """Limpa todas as tabelas antes da importação"""
    cursor = conn.cursor()
    try:
        cursor.execute("TRUNCATE TABLE operadoras")
        cursor.execute("TRUNCATE TABLE demonstracoes_contabeis")
        conn.commit()
        print("\nTabelas limpas com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"\nErro ao limpar tabelas: {e}")
    finally:
        cursor.close()

def importar_operadoras(conn, caminho_arquivo):
    """Importa dados das operadoras com todos os campos"""
    cursor = conn.cursor()
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8-sig') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')
            cabecalho = next(leitor)
            print("Cabeçalho encontrado:", cabecalho)
            
            linhas = list(leitor)
            total = len(linhas)
            
            for linha in tqdm(linhas, desc="Importando operadoras"):
                linha = [None if x == '' else x.strip() for x in linha]
                if len(linha) < 20:
                    linha += [None] * (20 - len(linha))
                
                dados = {
                    'registro_ans': linha[0],
                    'cnpj': linha[1],
                    'razao_social': linha[2],
                    'nome_fantasia': linha[3],
                    'modalidade': linha[4],
                    'logradouro': linha[5],
                    'numero': linha[6],
                    'complemento': linha[7],
                    'bairro': linha[8],
                    'cidade': linha[9],
                    'uf': linha[10],
                    'cep': linha[11],
                    'ddd': linha[12],
                    'telefone': linha[13],
                    'fax': linha[14],
                    'endereco_eletronico': linha[15],
                    'representante': linha[16],
                    'cargo_representante': linha[17],
                    'regiao_de_comercializacao': linha[18],
                    'data_registro_ans': formatar_data(linha[19]) if len(linha) > 19 else None
                }
                
                query = """
                INSERT INTO operadoras (
                    registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
                    logradouro, numero, complemento, bairro, cidade,
                    uf, cep, ddd, telefone, fax,
                    endereco_eletronico, representante, cargo_representante,
                    regiao_de_comercializacao, data_registro_ans
                ) VALUES (
                    %(registro_ans)s, %(cnpj)s, %(razao_social)s, %(nome_fantasia)s, %(modalidade)s,
                    %(logradouro)s, %(numero)s, %(complemento)s, %(bairro)s, %(cidade)s,
                    %(uf)s, %(cep)s, %(ddd)s, %(telefone)s, %(fax)s,
                    %(endereco_eletronico)s, %(representante)s, %(cargo_representante)s,
                    %(regiao_de_comercializacao)s, %(data_registro_ans)s
                )
                """
                cursor.execute(query, dados)
            
        conn.commit()
        print("\nOperadoras importadas com sucesso!")
        
    except Exception as e:
        conn.rollback()
        print(f"\nErro ao importar operadoras: {e}")
        print(f"Linha com problema: {linha}")
    finally:
        cursor.close()

def importar_demonstracoes(conn, caminho_arquivo, trimestre):
    """Importa dados contábeis com tratamento para múltiplos formatos de data"""
    cursor = conn.cursor()
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8-sig') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')
            next(leitor)
            
            primeira_linha = next(leitor)
            print(f"\nVerificando formato de data no arquivo {trimestre}:")
            print(f"Primeira linha - Data: '{primeira_linha[0]}'")
            arquivo.seek(0)
            next(leitor)
            
            for linha in tqdm(leitor, desc=f"Importando {trimestre}"):
                linha = [None if x == '' else x.strip().strip('"') for x in linha]
                data = converter_data(linha[0]) if linha[0] else None
                
                saldo_inicial = None
                if linha[4]:
                    try:
                        saldo_inicial = float(linha[4].replace('.', '').replace(',', '.'))
                    except:
                        pass
                
                saldo_final = None
                if linha[5]:
                    try:
                        saldo_final = float(linha[5].replace('.', '').replace(',', '.'))
                    except:
                        pass
                
                query = """
                INSERT INTO demonstracoes_contabeis (
                    data, reg_ans, cd_conta_contabil, descricao, 
                    vl_saldo_inicial, vl_saldo_final
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    data, linha[1], linha[2], linha[3],
                    saldo_inicial, saldo_final
                ))
            
        conn.commit()
        print(f"\n{trimestre} importado com sucesso!")
        
    except Exception as e:
        conn.rollback()
        print(f"\nErro ao importar {trimestre}: {e}")
        print(f"Linha problemática: {linha}")
    finally:
        cursor.close()

if __name__ == "__main__":
    caminhos = {
        'operadoras': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/operadoras/Relatorio_cadop.csv",
        'demonstracoes': {
            '1T2023': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/2023/1T2023/1T2023.csv",
            '2T2023': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/2023/2T2023/2T2023.csv",
            '3T2023': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/2023/3T2023/3T2023.csv",
            '4T2023': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/2023/4T2023/4T2023.csv",
            '1T2024': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/2024/1T2024/1T2024.csv",
            '2T2024': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/2024/2T2024/2T2024.csv",
            '3T2024': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/2024/3T2024/3T2024.csv",
            '4T2024': "D:/Projetos VS Code/TESTES DE NIVELAMENTO/3.TESTE DE BANCO DE DADOS/data/2024/4T2024/4T2024.csv"
        }
    }
    
    conn = conectar_banco()
    if conn:
        try:
            # Limpa todas as tabelas antes de importar
            limpar_tabelas(conn)
            
            # Importa operadoras
            importar_operadoras(conn, caminhos['operadoras'])
            
            # Importa demonstrações
            for trimestre, caminho in caminhos['demonstracoes'].items():
                importar_demonstracoes(conn, caminho, trimestre)
                
        finally:
            conn.close()
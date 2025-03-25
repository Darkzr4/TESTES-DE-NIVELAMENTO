import os
import csv
import zipfile
import pdfplumber

# Configurações
NOME_USUARIO = "Jefferson_Cavalcante"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = "downloads/Anexo I.pdf"
CSV_PATH = os.path.join(SCRIPT_DIR, f"Rol_Procedimentos_{NOME_USUARIO}.csv")
ZIP_PATH = os.path.join(SCRIPT_DIR, f"Teste_{NOME_USUARIO}.zip")

# Dicionário para substituição das abreviações
SUBSTITUICOES = {
    "OD": "Odontológico",
    "AMB": "Ambulatorial"
}

def limpar_texto(texto):
    if texto is None:
        return ""
    
    texto = texto.replace('\n', ' ').replace('\t', ' ')
    texto = ' '.join(texto.split())
    return texto

def processar_linha(linha):
    """Processa uma linha da tabela, aplicando as substituições necessárias"""
    if len(linha) >= 13:
        # Aplica a substituição nas colunas OD (índice 3) e AMB (índice 4)
        linha[3] = SUBSTITUICOES.get(linha[3], linha[3])  # Coluna OD
        linha[4] = SUBSTITUICOES.get(linha[4], linha[4])  # Coluna AMB
    return linha[:13]

def extrair_tabelas_pdf(pdf_path):
    """Extrai tabelas do PDF com limpeza de texto"""
    print("\nIniciando extração de tabelas...")
    dados = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                print(f"Processando página {i}...")
                
                tabelas = page.find_tables({
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "intersection_y_tolerance": 15
                })
                
                if tabelas:
                    for tabela in tabelas:
                        dados_tabela = tabela.extract()
                        
                        if dados_tabela and len(dados_tabela[0]) >= 13:
                            for linha in dados_tabela[1:]:
                                linha_limpa = [limpar_texto(celula) for celula in linha[:13]]
                                linha_processada = processar_linha(linha_limpa)
                                dados.append(linha_processada)
    
    except Exception as e:
        print(f"\nErro durante a extração: {str(e)}")
    
    print(f"\nTotal de registros extraídos: {len(dados)}")
    return dados

def salvar_csv(dados, csv_path):
    """Salva os dados em CSV formatado corretamente"""
    if not dados:
        print("\nNenhum dado válido para salvar")
        return False
    
    print(f"\nSalvando {len(dados)} registros no CSV...")
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            
            writer.writerow([
                "PROCEDIMENTO", "RN (alteração)", "VIGÊNCIA", "OD", "AMB", 
                "HCO", "HSO", "REF", "PAC", "DUT", 
                "SUBGRUPO", "GRUPO", "CAPÍTULO"
            ])
            
            writer.writerows(dados)
        
        print(f"Arquivo CSV salvo em: {os.path.abspath(csv_path)}")
        return True
    
    except Exception as e:
        print(f"\nErro ao salvar CSV: {str(e)}")
        return False

def criar_zip(csv_path, zip_path):
    """Cria o arquivo ZIP"""
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))
        print(f"\nArquivo ZIP criado em: {os.path.abspath(zip_path)}")
        return True
    except Exception as e:
        print(f"\nErro ao criar ZIP: {str(e)}")
        return False

def main():
    print("\n" + "="*50)
    print("PROCESSAMENTO DO ANEXO I - ANS")
    print("="*50)
    
    if not os.path.exists(PDF_PATH):
        print(f"\nERRO: Arquivo PDF não encontrado em:\n{PDF_PATH}")
        return
    
    dados = extrair_tabelas_pdf(PDF_PATH)
    
    if dados:
        if salvar_csv(dados, CSV_PATH):
            criar_zip(CSV_PATH, ZIP_PATH)
    else:
        print("\nAVISO: Nenhum dado foi extraído. Verifique o PDF.")

if __name__ == "__main__":
    main()
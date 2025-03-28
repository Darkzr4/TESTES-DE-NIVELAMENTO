# Script 01: Estruturação das pastas, download e extração dos arquivos necessários.

import os
import requests
import zipfile
from tqdm import tqdm

# Configurações
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
YEARS = ['2023', '2024']
BASE_URL = 'https://dadosabertos.ans.gov.br/FTP/PDA/'

def create_folders():
    os.makedirs(os.path.join(DATA_DIR, 'operadoras'), exist_ok=True)
    for year in YEARS:
        os.makedirs(os.path.join(DATA_DIR, year), exist_ok=True)

def download_file(url, destination):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Cria pasta com o nome do arquivo ZIP
        zip_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_path = os.path.join(extract_to, zip_name)
        os.makedirs(extract_path, exist_ok=True)
        
        # Extrai todos os arquivos
        for file in tqdm(zip_ref.namelist(), desc=f'Extraindo {os.path.basename(zip_path)}'):
            zip_ref.extract(file, extract_path)
        return extract_path

def safe_delete_zip(zip_path):
    try:
        os.remove(zip_path)
        print(f"Arquivo {os.path.basename(zip_path)} excluído com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir {os.path.basename(zip_path)}: {e}")

def download_and_extract_reports():
    for year in YEARS:
        print(f'\nProcessando relatórios de {year}...')
        for quarter in range(1, 5):
            filename = f'{quarter}T{year}.zip'
            url = f'{BASE_URL}demonstracoes_contabeis/{year}/{filename}'
            zip_dest = os.path.join(DATA_DIR, year, filename)
            extract_dir = os.path.join(DATA_DIR, year)
            
            # Verifica se já foi extraído
            extracted_dir = os.path.join(DATA_DIR, year, f'{quarter}T{year}')
            if os.path.exists(extracted_dir):
                print(f'{filename} já extraído, pulando...')
                # Verifica se o ZIP ainda existe e exclui
                if os.path.exists(zip_dest):
                    safe_delete_zip(zip_dest)
                continue
                
            # Download se necessário
            if not os.path.exists(zip_dest):
                try:
                    download_file(url, zip_dest)
                except Exception as e:
                    print(f'Erro ao baixar {filename}: {e}')
                    continue
            
            # Extração
            try:
                print(f'Extraindo {filename}...')
                extract_zip(zip_dest, extract_dir)
                print(f'{filename} extraído com sucesso!')
                
                # Exclui o ZIP após extração bem-sucedida
                safe_delete_zip(zip_dest)
            except Exception as e:
                print(f'Erro ao extrair {filename}: {e}')

# Baixa os dados cadastrais das operadoras
def download_operator_data():
    print('\nBaixando dados cadastrais das operadoras...')
    url = f'{BASE_URL}operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv'
    dest = os.path.join(DATA_DIR, 'operadoras', 'Relatorio_cadop.csv')
    
    if not os.path.exists(dest):
        try:
            download_file(url, dest)
            print('Dados cadastrais baixados com sucesso!')
        except Exception as e:
            print(f'Erro ao baixar dados cadastrais: {e}')
    else:
        print('Dados cadastrais já existem, pulando...')

def main():
    print("Iniciando download e extração dos dados da ANS...")
    create_folders()
    download_and_extract_reports()
    download_operator_data()
    print("\nProcesso concluído! Verifique a pasta 'data' para os resultados.")

if __name__ == '__main__':
    main()
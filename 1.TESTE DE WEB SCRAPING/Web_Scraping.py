import requests
import os
import zipfile

# URL do site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Configurações de diretórios
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
ZIP_FILE = os.path.join(DIRETORIO_ATUAL, "anexos.zip")

# Acessar a página
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a página: {e}")
    exit()

# Anexos para download
anexos = {
    "Anexo I.pdf": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",
    "Anexo II.pdf": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
}

# Download dos arquivos
for nome_arquivo, url_arquivo in anexos.items():
    try:
        with requests.get(url_arquivo, stream=True) as resposta:
            resposta.raise_for_status()

            caminho_arquivo = os.path.join(DOWNLOAD_DIR, nome_arquivo)

            with open(caminho_arquivo, 'wb') as arquivo:
                for chunk in resposta.iter_content(chunk_size=8192):
                    if chunk: 
                        arquivo.write(chunk)

            print(f"Download concluído: {nome_arquivo}")

    except Exception as e:
        print(f"Falha ao baixar {nome_arquivo}: {e}")

# Compactação
try:
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in os.listdir(DOWNLOAD_DIR):
            caminho_arquivo = os.path.join(DOWNLOAD_DIR, arquivo)
            zipf.write(caminho_arquivo, arquivo)

    print(f"Compactação concluída: {ZIP_FILE}")
    print(f"Tamanho do arquivo ZIP: {os.path.getsize(ZIP_FILE)/1024:.2f} KB")

except Exception as e:
    print(f"Erro ao criar arquivo ZIP: {e}")
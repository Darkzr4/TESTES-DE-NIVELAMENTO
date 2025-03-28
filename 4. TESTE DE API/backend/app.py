from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Carregar os dados do CSV
def carregar_dados():
    caminho_csv = 'backend/data/Relatorio_cadop.csv'
    # Lê o arquivo com encoding latin1
    df = pd.read_csv(
        caminho_csv,
        sep=';',
        encoding='latin1',
        dtype=str,
        keep_default_na=False
    )
    return df

# Rota principal
@app.route('/')
def home():
    return "Servidor da API de Operadoras ANS"

# Rota de busca
@app.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('termo', '').strip().lower()
    
    try:
        df = carregar_dados()
        
        mask = df.apply(
            lambda row: any(termo in str(cell).lower() for cell in row),
            axis=1
        )
        resultado = df[mask].head(50)
        
        def corrigir_codificacao(valor):
            if isinstance(valor, str):
                try:
                    return valor.encode('latin1').decode('utf-8')
                except:
                    return valor
            return valor
        
        resultado = resultado.applymap(corrigir_codificacao)
        
        # Converte para JSON
        json_data = resultado.where(pd.notnull(resultado), None).to_dict(orient='records')
        
        response = jsonify(json_data)
        response.headers.add('Content-Type', 'application/json; charset=utf-8')
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
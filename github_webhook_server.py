
from flask import Flask, request, jsonify

app = Flask(__name__)

# Rota para receber o webhook
@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # Pega os dados do webhook
    data = request.json
    print("Dados recebidos do GitHub:", data)

    # Processa os dados (adicionar lógica conforme necessário)
    response = {"message": "Webhook recebido com sucesso do GitHub!"}

    # Retorna uma resposta JSON
    return jsonify(response), 200

if __name__ == '__main__':
    # Inicia o servidor Flask
    
    app.run(host='0.0.0.0', port=5000)

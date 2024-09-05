# Usar uma imagem base do Python
FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requisitos
COPY requirements.txt .

# Instalar dependências
RUN pip install -r requirements.txt

# Copiar o código da aplicação para o diretório de trabalho
COPY github_webhook_server.py .

# Expor a porta que o servidor Flask vai usar
EXPOSE 5000

# Comando para rodar o servidor Flask
CMD ["python", "github_webhook_server.py"]

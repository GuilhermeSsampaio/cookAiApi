FROM python:3.11-slim

WORKDIR /app

# Combinar comandos RUN para reduzir camadas
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos '' appuser

# Copiar apenas os arquivos necessários primeiro
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar apenas os diretórios necessários
COPY ./database ./database
COPY ./models ./models
COPY ./routes ./routes
COPY ./services ./services
COPY ./utils ./utils
COPY main.py .
COPY .env .

# Ajustar permissões
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Adicionar healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
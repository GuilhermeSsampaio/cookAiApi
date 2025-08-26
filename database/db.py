from dotenv import load_dotenv  # Adicione esta importação
from urllib.parse import quote_plus

from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import os
from pathlib import Path


# Carrega o .env da raiz do projeto
root_dir = Path(__file__).parent.parent
load_dotenv(root_dir / ".env")


# Credenciais do banco
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

print(f"Conectando ao banco de dados em {DB_HOST}:{DB_PORT}/{DB_NAME} como usuário {DB_USER}")
# Construindo a URL de conexão de forma segura
DATABASE_URL = f"postgresql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}"

# Criando o engine com suporte a UTF-8
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"client_encoding": "utf8"}
)

def init_db():
    SQLModel.metadata.create_all(engine)
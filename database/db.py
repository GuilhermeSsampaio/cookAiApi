from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import os
from urllib.parse import quote_plus

# Credenciais do banco
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "cookai")

# Construindo a URL de conexão de forma segura
DATABASE_URL = f"postgresql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando o engine com suporte a UTF-8
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"client_encoding": "utf8"}
)

def init_db():
    SQLModel.metadata.create_all(engine)
from nt import environ
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
import os
from pathlib import Path

# Carrega o .env da raiz do projeto
root_dir = Path(__file__).parent.parent
load_dotenv(root_dir / ".env")

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

if os.getenv("ENV") == "test":
    print("\n\n ambiente: ",os.getenv("ENV"), "\n\n")
    print("Modo de teste ativado: o banco de dados será reiniciado a cada inicialização.")
     # Se estiver em modo de teste, reinicia o banco de dados
     # Cuidado: isso apagará todos os dados existentes!
    def init_db():
        SQLModel.metadata.drop_all(engine)  # Exclui todas as tabelas
        SQLModel.metadata.create_all(engine)  # Recria todas as tabelas
else:
    def init_db():
        SQLModel.metadata.create_all(engine)  # Cria as tabelas se não existirem
    
def get_session():
    with Session(engine) as session:
        yield session
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Contratacoes  # Importe a classe Contratacoes do arquivo models

# Cria a conexão com o banco de dados
engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Cria uma nova contratação
nova_contratacao = Contratacoes(
    User_id=5681316674,        # ID do usuário
    Plano_id=3,                # ID do plano
    Data_fim=datetime(2024, 10, 13)  # Data final da contratação
)

# Adiciona e confirma a nova contratação no banco de dados
session.add(nova_contratacao)
session.commit()
session.close()

print("Contratação cadastrada com sucesso!")



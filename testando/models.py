import telebot
from telebot import types
from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, Date, ForeignKey, CheckConstraint, BLOB
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Criação do engine de conexão com o SQLite
engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)

# Criação da base declarativa do SQLAlchemy
Base = declarative_base()

# Definição das tabelas com SQLAlchemy

class Users(Base):
    __tablename__ = 'users'
    
    User_Id = Column(Integer, primary_key=True)
    Username = Column(String(255), nullable=False)
    Name = Column(String(255), nullable=False)
    Tipo = Column(String(50), CheckConstraint("Tipo IN ('Ativo', 'Ex-ativo', 'não comprou')"), nullable=False)
    
    contratacoes = relationship("Contratacoes", back_populates="user")

class Planos(Base):
    __tablename__ = 'planos'
    
    Plano_id = Column(Integer, primary_key=True, autoincrement=True)
    Titulo = Column(String(40), nullable=False)
    Valor = Column(DECIMAL(10, 2), nullable=False)
    Descricao_Duracao = Column(String(40), nullable=False)
    Duracao = Column(Integer, nullable=False)
    Mensagem_personalizada = Column(Text)  # nullable=False pode ser adicionado se necessário

    contratacoes = relationship("Contratacoes", back_populates="plano")

class Apresentacao(Base):
    __tablename__ = 'apresentacao'
    
    apresentacao_id = Column(Integer, primary_key=True, autoincrement=True)
    Texto_1 = Column(Text)
    Texto_2 = Column(Text)
    Imagem = Column(BLOB)

class Contratacoes(Base):
    __tablename__ = 'contratacoes'
    
    Contratacao_id = Column(Integer, primary_key=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey('users.User_Id'))
    Plano_id = Column(Integer, ForeignKey('planos.Plano_id'))
    Data_inicio = Column(Date)
    Data_fim = Column(Date)

    user = relationship("Users", back_populates="contratacoes")
    plano = relationship("Planos", back_populates="contratacoes")

class Mensagens(Base):
    __tablename__ = 'mensagens'
    
    mensagens_id = Column(Integer, primary_key=True, autoincrement=True)
    mensangem_aguarde = Column(Text)
    mensangem_pix_1 = Column(Text)
    mensangem_pix_2 = Column(Text)
    mensangem_cartao_1 = Column(Text)
    mensangem_cartao_2 = Column(Text)
    mensangem_pagamento = Column(Text)
    mensangem_confirmacao = Column(Text)
    mensangem_nao_confirmacao = Column(Text)
    link_mercado_pago = Column(Text)
    mensagem_acesso_grupo = Column(Text)
    mensagem_para_todos = Column(Text)
    mensagem_para_ativos = Column(Text)
    mensagem_para_ex_ativos = Column(Text)
    mensagem_para_nao_pagantes = Column(Text)
    # mensagem_pos_pagamento= Column(Text)
    
class Comandos(Base):
    __tablename__ = 'comandos'  # Adicionar o nome da tabela
    comando_id = Column(Integer, primary_key=True, autoincrement=True)
    comando = Column(Text)



# Criação de todas as tabelas no banco de dados
Base.metadata.create_all(engine)

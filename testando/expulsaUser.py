from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users, Contratacoes  # Importe as classes Users e Contratacoes do arquivo models
import telebot

# Inicializa o bot do Telegram
bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

# Cria a conexão com o banco de dados
engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Obtém a data de hoje
data_atual = date.today()

# Consulta todas as contratações
contratacoes = session.query(Contratacoes).all()

# Itera sobre cada contratação
for contratacao in contratacoes:
    if contratacao.Data_fim <= data_atual:
        # A contratação expirou, então expulsar o usuário do grupo e atualizar o status
        user = session.query(Users).filter_by(User_Id=contratacao.User_id).first()

        if user and user.Tipo == 'Ativo':
            # Expulsar o usuário do grupo do Telegram
            try:
                bot.kick_chat_member('-4545092182', str(user.User_Id))
                bot.send_message(user.User_Id, "Sua contratação expirou e você foi removido do grupo.")
            except Exception as e:
                print(f"Erro ao expulsar o usuário {user.Username}: {str(e)}")

            # Atualizar o tipo de usuário para 'Ex-ativo'
            user.Tipo = 'Ex-ativo'
            session.commit()
            print(f"Usuário {user.Username} atualizado para Ex-ativo.")

        # Excluir a contratação do banco de dados
        session.delete(contratacao)
        session.commit()
        print(f"Contratação de {user.Username} excluída.")

# Fechar a sessão
session.close()
bot.polling()

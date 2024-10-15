import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import OfertaDeepWeb  

bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)

@bot.message_handler(commands=['ProgramaOfertaDeep'])
def programa_oferta_deep(message):
    bot.send_message(message.chat.id, "Digite a nova mensagem para a oferta Deep Web:")
    bot.register_next_step_handler(message, save_oferta_deep)

# Função para salvar ou atualizar a oferta no banco de dados
def save_oferta_deep(message):
    oferta_mensagem = message.text

    session = Session()
    try:
        # Verifica se já existe uma oferta
        existing_oferta = session.query(OfertaDeepWeb).first()

        if existing_oferta:
            # Atualiza a oferta existente
            existing_oferta.Mensagem = oferta_mensagem
            session.commit()
            bot.send_message(message.chat.id, "Oferta Deep Web atualizada com sucesso!")
        else:
            # Se não existir, cria uma nova
            nova_oferta = OfertaDeepWeb(Mensagem=oferta_mensagem)
            session.add(nova_oferta)
            session.commit()
            bot.send_message(message.chat.id, "Oferta Deep Web salva com sucesso!")

    except Exception as e:
        session.rollback()  # Rollback em caso de erro
        bot.send_message(message.chat.id, f"Erro ao salvar a oferta: {str(e)}")
    finally:
        session.close()

# Iniciar o bot
bot.polling()

import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Apresentacao  # Importe a classe Apresentacao do arquivo models

bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

# Criação do engine de conexão com o SQLite
engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)

# Variáveis globais para os textos
custom_text_1 = "Texto padrão 1"
custom_text_2 = "Texto padrão 2"
custom_image = None

# Comando /ProgramarStart
@bot.message_handler(commands=['ProgramarStart'])
def programar_start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Editar Texto 1', callback_data='editar_texto_1'))
    markup.add(types.InlineKeyboardButton('Editar Texto 2', callback_data='editar_texto_2'))
    markup.add(types.InlineKeyboardButton('Editar Imagem', callback_data='editar_imagem'))

    bot.send_message(message.chat.id, "Escolha o que você deseja editar:", reply_markup=markup)

# Captura a escolha de edição
@bot.callback_query_handler(func=lambda call: call.data in ['editar_texto_1', 'editar_texto_2', 'editar_imagem'])
def program_choice(call):
    if call.data == 'editar_texto_1':
        bot.send_message(call.message.chat.id, "Digite o novo Texto 1:")
        bot.register_next_step_handler(call.message, set_new_text_1)
    elif call.data == 'editar_texto_2':
        bot.send_message(call.message.chat.id, "Digite o novo Texto 2:")
        bot.register_next_step_handler(call.message, set_new_text_2)
    elif call.data == 'editar_imagem':
        bot.send_message(call.message.chat.id, "Envie a nova imagem que será usada.")
        bot.register_next_step_handler(call.message, set_new_image)

# Atualiza o Texto 1
def set_new_text_1(message):
    global custom_text_1
    custom_text_1 = message.text
    bot.send_message(message.chat.id, f"Texto 1 atualizado para: {custom_text_1}")

# Atualiza o Texto 2
def set_new_text_2(message):
    global custom_text_2
    custom_text_2 = message.text
    bot.send_message(message.chat.id, f"Texto 2 atualizado para: {custom_text_2}")

# Atualiza a imagem e oferece o botão para salvar
def set_new_image(message):
    global custom_image
    if message.content_type == 'photo':
        custom_image = message.photo[-1].file_id
        bot.send_message(message.chat.id, "Imagem atualizada com sucesso.")

        # Adiciona o botão para salvar a apresentação
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Salvar Apresentação', callback_data='salvar_apresentacao'))
        bot.send_message(message.chat.id, "Clique no botão abaixo para salvar a apresentação:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Por favor, envie uma imagem.")

# Salva a apresentação no banco de dados
def save_apresentacao(chat_id):
    session = Session()
    
    try:
        # Criação do objeto de apresentação
        nova_apresentacao = Apresentacao(Texto_1=custom_text_1, Texto_2=custom_text_2, Imagem=custom_image)
        
        # Adiciona e comita a nova apresentação
        session.add(nova_apresentacao)
        session.commit()
        
        bot.send_message(chat_id, "Apresentação salva com sucesso!")
    except Exception as e:
        session.rollback()  # Rollback em caso de erro
        bot.send_message(chat_id, f"Erro ao salvar a apresentação: {str(e)}")
    finally:
        session.close()

# Captura a escolha de salvar a apresentação
@bot.callback_query_handler(func=lambda call: call.data == 'salvar_apresentacao')
def save_apresentation_choice(call):
    save_apresentacao(call.message.chat.id)

# Iniciar o bot
bot.polling()

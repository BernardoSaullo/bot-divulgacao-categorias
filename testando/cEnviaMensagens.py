import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users, Mensagens  # Importe a classe Users e Mensagens do arquivo models

bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)

# Comando para programar mensagens
@bot.message_handler(commands=['Programar_Enviar_mensagem'])
def programa_enviar_mensagem(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Mensagem para Todos', callback_data='programar_todos'))
    markup.add(types.InlineKeyboardButton('Mensagem para Ativos', callback_data='programar_ativo'))
    markup.add(types.InlineKeyboardButton('Mensagem para Ex-ativos', callback_data='programar_exativo'))
    markup.add(types.InlineKeyboardButton('Mensagem para Não Comprou', callback_data='programar_naocomprou'))
    
    bot.send_message(message.chat.id, "Escolha o tipo de mensagem que deseja programar:", reply_markup=markup)

# Captura a escolha de programação de mensagem
@bot.callback_query_handler(func=lambda call: call.data.startswith('programar_'))
def escolher_tipo_mensagem(call):
    tipo = call.data.split('_')[1]
    if tipo == 'todos':
        bot.send_message(call.message.chat.id, "Digite a mensagem para Todos:")
        bot.register_next_step_handler(call.message, set_mensagem, 'mensagem_para_todos')
    elif tipo == 'ativo':
        bot.send_message(call.message.chat.id, "Digite a mensagem para Ativos:")
        bot.register_next_step_handler(call.message, set_mensagem, 'mensagem_para_ativos')
    elif tipo == 'exativo':
        bot.send_message(call.message.chat.id, "Digite a mensagem para Ex-ativos:")
        bot.register_next_step_handler(call.message, set_mensagem, 'mensagem_para_ex_ativos')
    elif tipo == 'naocomprou':
        bot.send_message(call.message.chat.id, "Digite a mensagem para Não Comprou:")
        bot.register_next_step_handler(call.message, set_mensagem, 'mensagem_para_nao_pagantes')

# Salva a mensagem programada no banco de dados
def set_mensagem(message, campo_mensagem):
    session = Session()
    
    try:
        # Busca a única entrada de mensagens (ou cria uma se não houver)
        mensagens_db = session.query(Mensagens).first()
        if not mensagens_db:
            mensagens_db = Mensagens()

        # Atualiza o campo correspondente no banco de dados
        setattr(mensagens_db, campo_mensagem, message.text)

        session.add(mensagens_db)
        session.commit()
        
        bot.send_message(message.chat.id, f"Mensagem para '{campo_mensagem.replace('_', ' ')}' programada com sucesso!")
    
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, f"Erro ao programar a mensagem: {str(e)}")
    
    finally:
        session.close()


# Comando para escolher para quem enviar as mensagens programadas
@bot.message_handler(commands=['enviar_mensagens_programadas'])
def escolher_tipo_envio_mensagem(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Enviar para Todos', callback_data='enviar_todos'))
    markup.add(types.InlineKeyboardButton('Enviar para Ativos', callback_data='enviar_ativos'))
    markup.add(types.InlineKeyboardButton('Enviar para Ex-ativos', callback_data='enviar_exativos'))
    markup.add(types.InlineKeyboardButton('Enviar para Não Pagantes', callback_data='enviar_naopagantes'))
    
    bot.send_message(message.chat.id, "Escolha para qual grupo de usuários deseja enviar a mensagem:", reply_markup=markup)

# Captura a escolha do grupo de usuários para enviar a mensagem
@bot.callback_query_handler(func=lambda call: call.data.startswith('enviar_'))
def enviar_mensagens(call):
    session = Session()

    # Busca a mensagem programada no banco de dados
    mensagens_db = session.query(Mensagens).first()
    if not mensagens_db:
        bot.send_message(call.message.chat.id, "Nenhuma mensagem programada encontrada.")
        session.close()
        return

    # Define o grupo de usuários com base no callback_data
    tipo_envio = call.data.split('_')[1]
    usuarios = None
    mensagem = None

    if tipo_envio == 'todos':
        usuarios = session.query(Users).all()
        mensagem = mensagens_db.mensagem_para_todos
    elif tipo_envio == 'ativos':
        usuarios = session.query(Users).filter_by(Tipo='Ativo').all()
        mensagem = mensagens_db.mensagem_para_ativos
    elif tipo_envio == 'exativos':
        usuarios = session.query(Users).filter_by(Tipo='Ex-ativo').all()
        mensagem = mensagens_db.mensagem_para_ex_ativos
    elif tipo_envio == 'naopagantes':
        usuarios = session.query(Users).filter_by(Tipo='não comprou').all()
        mensagem = mensagens_db.mensagem_para_nao_pagantes

    if not usuarios or not mensagem:
        bot.send_message(call.message.chat.id, "Nenhum usuário encontrado ou mensagem não programada para este grupo.")
        session.close()
        return

    # Envia a mensagem programada para o grupo selecionado
    for usuario in usuarios:
        bot.send_message(usuario.User_Id, mensagem)

    bot.send_message(call.message.chat.id, f"Mensagens enviadas com sucesso para o grupo: {tipo_envio.replace('_', ' ')}.")
    session.close()

# Iniciar o bot
bot.polling()

import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users, Planos, Base  # Importe a classe Planos do arquivo models

bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)


@bot.message_handler(commands=['ProgramaPlanos'])
def programa_planos(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Criar Plano', callback_data='criar_plano'))
    markup.add(types.InlineKeyboardButton('Deletar Plano', callback_data='deletar_plano'))
    
    bot.send_message(message.chat.id, "O que você deseja fazer?", reply_markup=markup)

# Criar ou deletar planos
@bot.callback_query_handler(func=lambda call: call.data in ['criar_plano', 'deletar_plano'])
def plano_choice(call):
    if call.data == 'criar_plano':
        bot.send_message(call.message.chat.id, "Digite o título do novo plano:")
        bot.register_next_step_handler(call.message, set_plano_title)
    elif call.data == 'deletar_plano':
        list_planos(call.message.chat.id)

# Captura título do plano
def set_plano_title(message):
    bot.send_message(message.chat.id, "Agora insira o valor do plano (em R$):")
    bot.register_next_step_handler(message, set_plano_valor, {'titulo': message.text})

# Captura valor do plano
def set_plano_valor(message, plano):
    plano['valor'] = float(message.text)  # Converte o valor para float
    bot.send_message(message.chat.id, "Agora insira a duração do plano (Ex: 1 semana: 7 dias, 1 mês: 30 dias, etc.):")
    bot.register_next_step_handler(message, set_plano_duracao, plano)

# Captura duração do plano
def set_plano_duracao(message, plano):
    plano['duracao'] = message.text
    bot.send_message(message.chat.id, "Agora insira uma descrição para o plano:")
    bot.register_next_step_handler(message, set_plano_descricao, plano)

# Captura descrição do plano
def set_plano_descricao(message, plano):
    plano['descricao'] = message.text
    bot.send_message(message.chat.id, "Agora insira uma mensagem personalizada para o plano:")
    bot.register_next_step_handler(message, save_plano, plano)

# Salva o plano no banco de dados
def save_plano(message, plano):
    plano['mensagem_personalizada'] = message.text

    # Adiciona o plano ao banco de dados
    session = Session()
    novo_plano = Planos(
        Titulo=plano['titulo'],
        Valor=plano['valor'],
        Descricao_Duracao=plano['descricao'],
        Duracao=plano['duracao'],
        Mensagem_personalizada=plano['mensagem_personalizada']  # Salva a mensagem personalizada
    )
    
    session.add(novo_plano)
    session.commit()
    session.close()

    bot.send_message(message.chat.id, f"Plano '{plano['titulo']}' criado com sucesso! Valor: R$ {plano['valor']}, Duração: {plano['duracao']}, Mensagem Personalizada: {plano['mensagem_personalizada']}.")

def list_planos(chat_id):
    session = Session()
    planos = session.query(Planos).all()
    session.close()

    if not planos:
        bot.send_message(chat_id, "Nenhum plano disponível para deletar.")
        return

    markup = types.InlineKeyboardMarkup()
    for plano in planos:
        markup.add(types.InlineKeyboardButton(f"{plano.Titulo} - R$ {plano.Valor} ({plano.Duracao})", callback_data=f"deletar_{plano.Plano_id}"))
    
    bot.send_message(chat_id, "Escolha o plano que deseja deletar:", reply_markup=markup)


# Comando /planos (listar planos)
@bot.message_handler(commands=['planos'])
def listar_planos(message):
    session = Session()
    planos = session.query(Planos).all()
    session.close()

    if not planos:
        bot.send_message(message.chat.id, "Nenhum plano disponível no momento.")
        return

    markup = types.InlineKeyboardMarkup()

    # Lista todos os planos disponíveis
    for plano in planos:
        markup.add(types.InlineKeyboardButton(f"{plano.Titulo} - R$ {plano.Valor} ({plano.Duracao} dias)", callback_data=f"plano_{plano.Plano_id}"))

    bot.send_message(message.chat.id, "Escolha um plano para ver as formas de pagamento:", reply_markup=markup)

# Manipula o clique em um plano para mostrar as formas de pagamento
@bot.callback_query_handler(func=lambda call: call.data.startswith('plano_'))
def escolher_forma_pagamento(call):
    plano_id = int(call.data.split('_')[1])

    session = Session()
    plano = session.query(Planos).filter_by(Plano_id=plano_id).first()
    session.close()

    if plano:
        markup = types.InlineKeyboardMarkup()
        pix_button = types.InlineKeyboardButton(f"PIX - R$ {plano.Valor}", callback_data=f"pix_{plano_id}")
        cartao_button = types.InlineKeyboardButton(f"Cartão - R$ {plano.Valor}", callback_data=f"cartao_{plano_id}")
        markup.add(pix_button, cartao_button)

        bot.send_message(call.message.chat.id, f"Você escolheu o plano '{plano.Titulo}'. Escolha sua forma de pagamento:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "Plano não encontrado.")

# Manipula o clique em PIX ou Cartão e confirma o pagamento
@bot.callback_query_handler(func=lambda call: call.data.startswith(('pix_', 'cartao_')))
def confirmar_pagamento(call):
    plano_id = int(call.data.split('_')[1])

    session = Session()
    plano = session.query(Planos).filter_by(Plano_id=plano_id).first()
    session.close()

    if plano:
        if call.data.startswith('pix_'):
            bot.send_message(call.message.chat.id, f"Você escolheu pagar via PIX. O valor é de R$ {plano.Valor}. Aqui estão as instruções para o pagamento via PIX.")
            # Aqui você pode adicionar as instruções específicas de pagamento via PIX
        elif call.data.startswith('cartao_'):
            bot.send_message(call.message.chat.id, f"Você escolheu pagar via Cartão. O valor é de R$ {plano.Valor}. Aqui estão as instruções para o pagamento via Cartão.")
            # Aqui você pode adicionar as instruções específicas de pagamento via Cartão
    else:
        bot.send_message(call.message.chat.id, "Plano não encontrado.")

# Inicia o bot
bot.polling()   

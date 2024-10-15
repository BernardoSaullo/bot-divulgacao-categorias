import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Mensagens  # Importe a classe Mensagens do arquivo models

bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)

# Comando para programar as mensagens de pagamento
@bot.message_handler(commands=['Programa_Mensagens_Pagamento'])
def programa_mensagens_pagamento(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Mensagem Aguarde', callback_data='mensagem_aguarde'))
    markup.add(types.InlineKeyboardButton('Mensagem PIX 1', callback_data='mensagem_pix_1'))
    markup.add(types.InlineKeyboardButton('Mensagem PIX 2', callback_data='mensagem_pix_2'))
    markup.add(types.InlineKeyboardButton('Mensagem Cartão 1', callback_data='mensagem_cartao_1'))
    markup.add(types.InlineKeyboardButton('Mensagem Cartão 2', callback_data='mensagem_cartao_2'))
    markup.add(types.InlineKeyboardButton('Mensagem Pagamento', callback_data='mensagem_pagamento'))
    markup.add(types.InlineKeyboardButton('Mensagem Confirmação', callback_data='mensagem_confirmacao'))
    markup.add(types.InlineKeyboardButton('Mensagem Não Confirmação', callback_data='mensagem_nao_confirmacao'))
    markup.add(types.InlineKeyboardButton('Link Mercado Pago', callback_data='link_mercado_pago'))
    markup.add(types.InlineKeyboardButton('Mensagem Acesso ao Grupo', callback_data='mensagem_acesso_grupo'))
    
    bot.send_message(message.chat.id, "Escolha qual mensagem deseja programar:", reply_markup=markup)

# Captura a escolha do campo de mensagem a ser configurado
@bot.callback_query_handler(func=lambda call: call.data.startswith('mensagem_'))
def escolher_mensagem_pagamento(call):
    campo_mensagem = call.data
    mensagens_map = {
        'mensagem_aguarde': 'Mensagem Aguarde',
        'mensagem_pix_1': 'Mensagem PIX 1',
        'mensagem_pix_2': 'Mensagem PIX 2',
        'mensagem_cartao_1': 'Mensagem Cartão 1',
        'mensagem_cartao_2': 'Mensagem Cartão 2',
        'mensagem_pagamento': 'Mensagem de Pagamento',
        'mensagem_confirmacao': 'Mensagem de Confirmação',
        'mensagem_nao_confirmacao': 'Mensagem de Não Confirmação',
        'link_mercado_pago': 'Link Mercado Pago',
        'mensagem_acesso_grupo': 'Mensagem de Acesso ao Grupo'
    }

    bot.send_message(call.message.chat.id, f"Digite a nova {mensagens_map[campo_mensagem]}:")
    bot.register_next_step_handler(call.message, set_mensagem_pagamento, campo_mensagem)

# Função para salvar a mensagem no banco de dados
def set_mensagem_pagamento(message, campo_mensagem):
    session = Session()

    try:
        # Busca ou cria uma entrada de Mensagens no banco de dados
        mensagens_db = session.query(Mensagens).first()
        if not mensagens_db:
            mensagens_db = Mensagens()

        # Atualiza o campo específico da mensagem no banco de dados
        setattr(mensagens_db, campo_mensagem.replace('mensagem_', 'mensangem_'), message.text)

        session.add(mensagens_db)
        session.commit()

        bot.send_message(message.chat.id, "Mensagem configurada com sucesso!")
    
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, f"Erro ao salvar a mensagem: {str(e)}")
    
    finally:
        session.close()

# Iniciar o bot
bot.polling()

import telebot
from telebot import types

bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

# Comando /pagamentos
@bot.message_handler(commands=['pagamentos'])
def handle_pagamentos(message):
    markup = types.InlineKeyboardMarkup()
    
    # Adiciona botões de escolha para pagamento (PIX e Cartão)
    pix_button = types.InlineKeyboardButton("PIX", callback_data="pagamento_pix")
    cartao_button = types.InlineKeyboardButton("Cartão", callback_data="pagamento_cartao")
    
    markup.add(pix_button, cartao_button)
    
    # Envia a mensagem com os botões
    bot.send_message(message.chat.id, "Qual sua forma de pagamento?", reply_markup=markup)

# Manipula o clique nos botões
@bot.callback_query_handler(func=lambda call: call.data in ['pagamento_pix', 'pagamento_cartao'])
def handle_payment_choice(call):
    if call.data == "pagamento_pix":
        bot.send_message(call.message.chat.id, "Você escolheu PIX. Aqui estão as informações de pagamento.")
        # Adicione aqui as informações específicas de pagamento via PIX
    elif call.data == "pagamento_cartao":
        bot.send_message(call.message.chat.id, "Você escolheu Cartão. Aqui estão as informações de pagamento.")
        # Adicione aqui as informações específicas de pagamento via Cartão

# Inicia o bot
bot.polling()

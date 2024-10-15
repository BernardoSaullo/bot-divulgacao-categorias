import mercadopago
import telebot
from telebot import types
from flask import Flask, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Planos 
from decimal import Decimal
# Testando integração do fluxo 2 com 3
app = Flask(__name__)
bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)

# Função para gerar link de pagamento usando Mercado Pago
def gerar_link_pagamento(plano_id, valor_plano):
    sdk = mercadopago.SDK("TEST-6310058720351952-100822-e567773f1a6b76ebfc89a9376427a402-1957499458")

    # Converte o valor para float, necessário para o Mercado Pago
    valor_plano_float = float(valor_plano)

    payment_data = {
        "items": [
            {"id": str(plano_id), "title": f"Plano {plano_id}", "quantity": 1, "currency_id": "BRL", "unit_price": valor_plano_float}
        ],
        "back_urls": {
            "success": "http://127.0.0.1:5000/pagamento_concluido",
            "failure": "http://127.0.0.1:5000/pagamento_falhou",
            "pending": "http://127.0.0.1:5000/pagamento_pendente",
        },
    }

    result = sdk.preference().create(payment_data)
    payment = result["response"]
    link_iniciar_pagamento = payment["init_point"]
    payment_id = payment["id"]  # Captura o payment_id


    print(f"Link de pagamento gerado: {link_iniciar_pagamento}")
    
    return link_iniciar_pagamento

@app.route('/pagamento_concluido')
def pagamento_concluido():
    # Exibir no terminal que o pagamento foi aprovado
    print("Pagamento aprovado!")
    return '', 204

@app.route('/pagamento_falhou')
def pagamento_falhou():
    # Exibir no terminal que o pagamento foi rejeitado
    print("Pagamento rejeitado!")
    return '', 204

@app.route('/pagamento_pendente')
def pagamento_pendente():
    # Exibir no terminal que o pagamento está pendente
    print("Pagamento pendente!")
    return '', 204

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
        cartao_button = types.InlineKeyboardButton(f"Cartão - R$ {plano.Valor}", callback_data=f"cartao_{plano_id}")
        markup.add(cartao_button)

        bot.send_message(call.message.chat.id, f"Você escolheu o plano '{plano.Titulo}'. Escolha sua forma de pagamento:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "Plano não encontrado.")

# Manipula o clique em Cartão e gera o link de pagamento
@bot.callback_query_handler(func=lambda call: call.data.startswith('cartao_'))
def gerar_pagamento_cartao(call):
    plano_id = int(call.data.split('_')[1])

    session = Session()
    plano = session.query(Planos).filter_by(Plano_id=plano_id).first()
    session.close()

    if plano:
        # Gera o link de pagamento do Mercado Pago
        link_pagamento = gerar_link_pagamento(plano_id, plano.Valor)

        # Mostra o botão com o link de pagamento
        markup = types.InlineKeyboardMarkup()
        botao_pagamento = types.InlineKeyboardButton("Clique aqui para efetuar o pagamento", url=link_pagamento)
        confirmar_button = types.InlineKeyboardButton("Confirma pagamento", callback_data=f"confirma_pagamento_{plano_id}")
        markup.add(botao_pagamento)
        markup.add(confirmar_button)

        bot.send_message(call.message.chat.id, "Clique no botão abaixo para efetuar o pagamento:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "Plano não encontrado.")

# Verificar se o pagamento foi aprovado
@bot.callback_query_handler(func=lambda call: call.data.startswith('confirma_pagamento_'))
def confirmar_pagamento(call):
    payment_id = call.data.split('_')[2]  # Obter payment_id do callback_data

    # Verifique o status do pagamento na API do Mercado Pago
    status_pagamento = verificar_status_pagamento(payment_id)

    if status_pagamento == 'approved':
        bot.send_message(call.message.chat.id, "Pagamento confirmado com sucesso!")
    else:
        bot.send_message(call.message.chat.id, f"Pagamento não foi confirmado. Status: {status_pagamento}. Tente novamente.")

def verificar_status_pagamento(payment_id):
    sdk = mercadopago.SDK("TEST-6310058720351952-100822-e567773f1a6b76ebfc89a9376427a402-1957499458")
    
    # Consultar a API para obter informações do pagamento
    payment_info = sdk.payment().get(payment_id)
    
    # Retorna o status do pagamento
    return payment_info["response"]["status"]  # Pode retornar 'approved', 'rejected', 'pending', etc.
# Inicia o bot
if __name__ == '__main__':
    bot.polling()
    app.run(debug=True)

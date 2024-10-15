import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users, Planos  # Importando suas classes de modelo

# Inicialização do bot
bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

# Criação do engine e sessão do banco de dados
engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

custom_text_1 = "Texto padrão 1"
custom_text_2 = "Texto padrão 2"
custom_image = None

# Função para armazenar as informações do usuário
def store_user_info(user_id, username, first_name, last_name):
    user = session.query(Users).filter_by(User_Id=user_id).first()
    
    if not user:
        user = Users(User_Id=user_id, Username=username or "Não informado", Name=f"{first_name} {last_name}", Tipo="não comprou")
        session.add(user)
        session.commit()

## /start
# Comando /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Armazena as informações do usuário
    store_user_info(user_id, username, first_name, last_name)

    bot.send_message(message.chat.id, f"Bem-vindo {first_name}!")
    if custom_image:
        bot.send_photo(message.chat.id, custom_image)

    bot.send_message(message.chat.id, custom_text_1)
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Clique aqui para acessar", callback_data="acessar")
    markup.add(button)

    msg = bot.send_message(message.chat.id, custom_text_2, reply_markup=markup)

# Comando /ProgramarStart (editar textos e imagens)
@bot.message_handler(commands=['ProgramarStart'])
def programar_start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Editar Texto 1', callback_data='editar_texto_1'))
    markup.add(types.InlineKeyboardButton('Editar Texto 2', callback_data='editar_texto_2'))
    markup.add(types.InlineKeyboardButton('Editar Imagem', callback_data='editar_imagem'))

    bot.send_message(message.chat.id, "Escolha o que você deseja editar:", reply_markup=markup)

# Captura a escolha de edição (texto ou imagem)
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

# Atualiza a imagem
def set_new_image(message):
    if message.content_type == 'photo':
        global custom_image
        custom_image = message.photo[-1].file_id
        bot.send_message(message.chat.id, "Imagem atualizada com sucesso.")
    else:
        bot.send_message(message.chat.id, "Por favor, envie uma imagem.")

# Comando /show_users (mostrar informações dos usuários)
@bot.message_handler(commands=['show_users'])
def show_users(message):
    if message.from_user.id == 1798334869:  # Apenas para o administrador
        users = session.query(Users).all()
        if users:
            for user in users:
                bot.send_message(message.chat.id, 
                    f"ID: {user.User_Id}, Username: {user.Username}, Nome: {user.Name}")
        else:
            bot.send_message(message.chat.id, "Nenhum usuário registrado até o momento.")
    else:
        bot.send_message(message.chat.id, "Você não tem permissão para ver os dados.")

# Remover mensagem de acesso
# Manipulador para o callback do botão "Clique aqui para acessar"
@bot.callback_query_handler(func=lambda call: call.data == "acessar")
def acessar_callback(call):
    bot.send_message(call.message.chat.id, "Acesso concedido!")

    # Listar os planos disponíveis
    planos = session.query(Planos).all()
    if not planos:
        bot.send_message(call.message.chat.id, "Nenhum plano disponível.")
    else:
        markup = types.InlineKeyboardMarkup()
        for plano in planos:
            markup.add(types.InlineKeyboardButton(f"{plano.Titulo} - {plano.Valor} R$ ({plano.Descricao_Duracao})", callback_data=f"selecionar_{plano.Plano_id}"))
        bot.send_message(call.message.chat.id, "Escolha um plano:", reply_markup=markup)

# Selecionar plano (esta função já estava implementada)
@bot.callback_query_handler(func=lambda call: call.data.startswith('selecionar_'))
def selecionar_plano(call):
    plano_id = int(call.data.split('_')[1])
    plano_selecionado = session.query(Planos).get(plano_id)
    bot.send_message(call.message.chat.id, f"Você selecionou o plano:\nTítulo: {plano_selecionado.Titulo}\nValor: {plano_selecionado.Valor} R$\nDuração: {plano_selecionado.Descricao_Duracao}")

## planos
# Comando /ProgramaPlanos (gerenciamento de planos)
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
        planos = session.query(Planos).all()
        if len(planos) == 0:
            bot.send_message(call.message.chat.id, "Nenhum plano disponível para deletar.")
        else:
            markup = types.InlineKeyboardMarkup()
            for plano in planos:
                markup.add(types.InlineKeyboardButton(f"{plano.Titulo} - {plano.Valor} R$ ({plano.Descricao_Duracao})", callback_data=f"deletar_{plano.Plano_id}"))
            bot.send_message(call.message.chat.id, "Escolha o plano que deseja deletar:", reply_markup=markup)

# Captura título do plano
def set_plano_title(message):
    bot.send_message(message.chat.id, "Agora insira o valor do plano (em R$):")
    bot.register_next_step_handler(message, set_plano_valor, {'titulo': message.text})

# Captura valor do plano
def set_plano_valor(message, plano):
    plano['valor'] = message.text
    bot.send_message(message.chat.id, "Agora insira a duração do plano (Ex: 1 semana, 1 mês, etc.):")
    bot.register_next_step_handler(message, set_plano_duracao, plano)

# Captura duração do plano
def set_plano_duracao(message, plano):
    plano_obj = Planos(Titulo=plano['titulo'], Valor=plano['valor'], Descricao_Duracao=message.text, Duracao=0)  # O valor de Duracao pode ser definido conforme necessário
    session.add(plano_obj)
    session.commit()
    bot.send_message(message.chat.id, f"Plano '{plano['titulo']}' criado com sucesso! Valor: {plano['valor']} R$, Duração: {message.text}.")

# Deletar plano
@bot.callback_query_handler(func=lambda call: call.data.startswith('deletar_'))
def delete_plano(call):
    plano_id = int(call.data.split('_')[1])
    plano_deletado = session.query(Planos).get(plano_id)
    if plano_deletado:
        session.delete(plano_deletado)
        session.commit()
        bot.send_message(call.message.chat.id, f"Plano '{plano_deletado.Titulo}' deletado com sucesso!")
    else:
        bot.send_message(call.message.chat.id, "Plano não encontrado.")

# Comando /planos (listar planos)
@bot.message_handler(commands=['planos'])
def listar_planos(message):
    planos = session.query(Planos).all()
    if not planos:
        bot.send_message(message.chat.id, "Nenhum plano disponível.")
    else:
        markup = types.InlineKeyboardMarkup()
        for plano in planos:
            markup.add(types.InlineKeyboardButton(f"{plano.Titulo} - {plano.Valor} R$ ({plano.Descricao_Duracao})", callback_data=f"selecionar_{plano.Plano_id}"))
        bot.send_message(message.chat.id, "Escolha um plano:", reply_markup=markup)

# Inicia o bot
bot.polling()

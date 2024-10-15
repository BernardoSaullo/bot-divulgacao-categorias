import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users  # Certifique-se de que a classe Users está no arquivo models.py

custom_text_1 = "Texto padrão 1"
custom_text_2 = "Texto padrão 2"
custom_image = None
users_data = {}  # Definindo o dicionário para armazenar dados de usuários

bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

engine = create_engine('sqlite:///bot_telegram_v1.db', echo=True)
Session = sessionmaker(bind=engine)

# Comando /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "Não informado"
    first_name = message.from_user.first_name if message.from_user.first_name else "Não informado"
    last_name = message.from_user.last_name if message.from_user.last_name else "Não informado"
    tipo_usuario = "Ativo"  # Define o tipo como 'Ativo' por padrão

    # Criando uma nova sessão para interagir com o banco de dados
    session = Session()

    # Verifica se o usuário já está cadastrado
    existing_user = session.query(Users).filter_by(User_Id=user_id).first()

    if existing_user is None:
        # Adiciona o novo usuário ao banco de dados
        novo_usuario = Users(User_Id=user_id, Username=username, Name=first_name, Tipo=tipo_usuario)
        session.add(novo_usuario)
        session.commit()
        bot.send_message(message.chat.id, f"Bem-vindo {first_name}! Você foi cadastrado com sucesso.")
    else:
        bot.send_message(message.chat.id, f"Bem-vindo de volta {existing_user.Name}!")

    # Fechando a sessão
    session.close()

    # Mensagens padrão
    if custom_image:
        bot.send_photo(message.chat.id, custom_image)

    bot.send_message(message.chat.id, custom_text_1)
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Clique aqui para acessar", callback_data="acessar")
    markup.add(button)

    msg = bot.send_message(message.chat.id, custom_text_2, reply_markup=markup)
    users_data[message.chat.id] = {}  # Certifique-se de que o dicionário é inicializado
    users_data[message.chat.id]['msg_id'] = msg.message_id


@bot.message_handler(commands=['show_users'])
def show_users(message):
    session = Session()
    users = session.query(Users).all()
    if users:
        for user in users:
            bot.send_message(message.chat.id, f"ID: {user.User_Id}, Username: {user.Username}, Nome: {user.Name}, Tipo: {user.Tipo}")
    else:
        bot.send_message(message.chat.id, "Nenhum usuário registrado até o momento.")
    session.close()


# Inicia o bot
bot.polling()

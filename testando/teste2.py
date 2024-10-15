import telebot

# Substitua 'YOUR_BOT_TOKEN' pelo seu token do bot
bot = telebot.TeleBot(token='8182494445:AAHYrfXqjCCZJW8hdLDQ9SYix6ISRRBKXFM', parse_mode='HTML')

# ID do chat (grupo) e ID do usuário a ser expulso
chat_id = '-4545092182'  # Substitua pelo ID do seu grupo
user_id = '5681316674'  # Substitua pelo ID do usuário que você deseja expulsar

try:
    # Expulsa o usuário do grupo
    bot.kick_chat_member(chat_id, user_id)
    print(f"Usuário {user_id} expulso com sucesso do grupo {chat_id}.")
except Exception as e:
    print(f"Erro ao expulsar o usuário: {str(e)}")

# Inicie o bot
bot.polling()

import mysql.connector
from mysql.connector import Error
import telebot

def conectar_ao_banco():
    try:
   
       return mysql.connector.connect(
                host="103.199.185.155",
                user="usuario_remoto",
                password="nova_senha",
                database="ItsInvictus2"
            )
        

    except mysql.connector.Error as err:
        return err
    

bot = telebot.TeleBot(token="8104670349:AAEeYpiEhMXwmBwPuXG3y8x3qSesbSuFGOc", parse_mode='HTML')

aguardando_adm_id = {}
aguardando_exclusao = {}
aguardando_edicao_msg = {}
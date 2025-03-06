import mysql.connector
from mysql.connector import Error
import telebot

def conectar_ao_banco():
    try:
   
       return mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="root",
                database="ItsInvictus2"
            )
        

    except mysql.connector.Error as err:
        return err
    

bot = telebot.TeleBot(token="7754411017:AAEns1ic-BClUs6ETcywg1mJ-GRIo7DTQGY", parse_mode='HTML')

aguardando_adm_id = {}
aguardando_exclusao = {}
aguardando_edicao_msg = {}

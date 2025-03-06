import random
import time
import html
import mysql.connector
import datetime

from config import conectar_ao_banco, bot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def carregar_dados():
    global grupos_adultos
    global grupos_fixados_adultos

    global grupos_gerais
    global grupos_fixados_gerais

    global mensagem_lista

    # Estabelece a conexão com o banco
    conn = conectar_ao_banco()
    if conn is None:
        print("❌ Não foi possível conectar ao banco de dados.")
        return
    try:
        cursor = conn.cursor()

        # Busca dados no banco de dados para grupos aprovados
        cursor.execute("SELECT id, nome, link FROM grupos_e_canais WHERE apro = True and categoria = 'Adulto'")
        resultados_adultos = cursor.fetchall()

        cursor.execute("SELECT id, nome, link FROM grupos_e_canais WHERE apro = True and categoria = 'Geral'")
        resultados_gerais = cursor.fetchall()

        # Consulta para grupos fixados
        cursor.execute("SELECT id, nome, link FROM fixados_adulto")
        grupos_fixados_adultos_resultados = cursor.fetchall()

        cursor.execute("SELECT id, nome, link FROM fixados_geral")
        grupos_fixados_gerais_resultados = cursor.fetchall()

        # Criação dos dicionários
        grupos_adultos = {id: [nome, link] for id, nome, link in resultados_adultos}
        grupos_fixados_adultos = {id: [nome, link] for id, nome, link in grupos_fixados_adultos_resultados}

        grupos_gerais = {id: [nome, link] for id, nome, link in resultados_gerais}
        grupos_fixados_gerais = {id: [nome, link] for id, nome, link in grupos_fixados_gerais_resultados}

        cursor.execute("SELECT Mensagem_Lista FROM mensagens LIMIT 1")
        mensagem_lista = cursor.fetchone()


        print("Dados carregados às 5:00.")

    except mysql.connector.Error as err:
        print(f"Erro ao consultar o banco de dados: {err}")

    finally:
        # Fecha a conexão com o banco de dados
        conn.close()



# Função para monitorar e enviar a lista de grupos
def lista_adulta():
    global grupos_adultos
    global grupos_fixados_adultos

    global mensagem_lista

    if not grupos_adultos:  
        print("❌ A lista de grupos está vazia. Carregue os dados antes de chamar essa função.")
        return
    

    conn = conectar_ao_banco()
    if conn is None:
        print("❌ Não foi possível conectar ao banco de dados.")
        return

    cursor = conn.cursor()
    i = 0
    print("Enviando lista de grupos adultos...")
    print('-' * 50)
    for grupo_id in grupos_adultos.keys():
        i += 1
        if i == 10:
            time.sleep(5)
            i = 0
        try:
            # Seleciona 20 grupos aleatoriamente
            chaves_aleatorias = random.sample(list(grupos_adultos.keys()), min(30, len(grupos_adultos)))
            grupos_selecionados = {chave: grupos_adultos[chave] for chave in chaves_aleatorias}

            # Cria o markup para os botões
            markup = InlineKeyboardMarkup()

            # Se houver grupos fixados, adicione-os primeiro
            if grupos_fixados_adultos:
                # Adiciona botões com os grupos fixados
                buttons = [InlineKeyboardButton(text=f" {html.escape(grupo[0])} ", url=grupo[1]) for grupo in grupos_fixados_adultos.values()]

                # Adiciona o primeiro botão fixado na primeira linha

            # Função para adicionar botões em pares de 2
            def adicionar_botoes_em_pares(grupos):
                botao_par = []  # Lista para armazenar pares de botões
                for chave, valores in grupos:
                    nome, link = valores
                    botao_par.append(InlineKeyboardButton(text=nome, url=link))

                    # Quando atingimos 2 botões, os coloca em uma nova linha
                    if len(botao_par) == 2:
                        markup.add(*botao_par)  # Adiciona os dois botões na linha
                        botao_par = []  # Reseta a lista para o próximo par

                # Caso reste 1 botão na última linha, adiciona ele sozinho
                if botao_par:
                    markup.add(*botao_par)
            if len(buttons) >= 1:
                markup.add(buttons[0])  # 1 botão na primeira linha


            # Adicionar os 10 primeiros
            adicionar_botoes_em_pares(list(grupos_selecionados.items())[:10])  # 10 primeiros

            # Adiciona o segundo botão fixado após os 10 primeiros
            if len(buttons) > 1:
                markup.add(buttons[1])  # Adiciona o segundo botão fixado na segunda linha

            # Adicionar os 10 intermediários
            adicionar_botoes_em_pares(list(grupos_selecionados.items())[10:20])  # 10 intermediários

            # Adicionar os 10 últimos
            if len(buttons) >= 1:
                    markup.add(buttons[2])  # 1 botão na primeira linha
            adicionar_botoes_em_pares(list(grupos_selecionados.items())[20:])   # 10 últimos


            markup.add(
                InlineKeyboardButton('⚙ 𝗔𝗗𝗜𝗖𝗜𝗢𝗡𝗔𝗥 𝗚𝗥𝗨𝗣𝗢 🔗', url="https://t.me/BravusListBot")
            )

            # Envia a mensagem e armazena a resposta
            msg = bot.send_message(grupo_id, 'Categoria Adulta', reply_markup=markup, parse_mode='HTML')
            print(f"✅ Lista enviada para o grupo {grupo_id}.")
            
            # Salva os detalhes da mensagem enviada no banco de dados
            cursor.execute("""
                INSERT INTO listas_rastreadas (chat_id, mensagem_id, data_envio)
                VALUES (%s, %s, %s)
            """, (grupo_id, msg.message_id, datetime.datetime.now()))
            conn.commit()
            print(f"✅ Registro inserido na tabela ListaRastreada para o grupo {grupo_id}.")
        except Exception as e:

            print(f"❌ Erro ao enviar mensagem para o grupo {grupo_id}: {e}")

            # Fechar a conexão do banco
    cursor.close()
    conn.close()


def lista_geral():
    global grupos_gerais
    global grupos_fixados_gerais
    
    global mensagem_lista

    if not grupos_gerais:
        print("❌ A lista de grupos está vazia. Carregue os dados antes de chamar essa função.")
        return

    conn = conectar_ao_banco()
    if conn is None:
        print("❌ Não foi possível conectar ao banco de dados.")
        return

    cursor = conn.cursor()
    i = 0
    print("Enviando lista de grupos Gerais...")
    print('-' * 50)
    for grupo_id in grupos_gerais.keys():
        i += 1
        if i == 10:
            time.sleep(5)
            i = 0
        try:
            # Seleciona 20 grupos aleatoriamente
            chaves_aleatorias = random.sample(list(grupos_gerais.keys()), min(30, len(grupos_gerais)))
            grupos_selecionados = {chave: grupos_gerais[chave] for chave in chaves_aleatorias}

            # Cria o markup para os botões
            markup = InlineKeyboardMarkup()

            # Se houver grupos fixados, adicione-os primeiro
            if grupos_fixados_gerais:
                # Adiciona botões com os grupos fixados
                buttons = [InlineKeyboardButton(text=f" {html.escape(grupo[0])} ", url=grupo[1]) for grupo in grupos_fixados_gerais.values()]

                # Adiciona o primeiro botão fixado na primeira linha

            # Função para adicionar botões em pares de 2
            def adicionar_botoes_em_pares(grupos):
                botao_par = []  # Lista para armazenar pares de botões
                for chave, valores in grupos:
                    nome, link = valores
                    botao_par.append(InlineKeyboardButton(text=nome, url=link))

                    # Quando atingimos 2 botões, os coloca em uma nova linha
                    if len(botao_par) == 2:
                        markup.add(*botao_par)  # Adiciona os dois botões na linha
                        botao_par = []  # Reseta a lista para o próximo par

                # Caso reste 1 botão na última linha, adiciona ele sozinho
                if botao_par:
                    markup.add(*botao_par)
            if len(buttons) >= 1:
                markup.add(buttons[0])  # 1 botão na primeira linha


            # Adicionar os 10 primeiros
            adicionar_botoes_em_pares(list(grupos_selecionados.items())[:10])  # 10 primeiros

            # Adiciona o segundo botão fixado após os 10 primeiros
            if len(buttons) > 1:
                markup.add(buttons[1])  # Adiciona o segundo botão fixado na segunda linha

            # Adicionar os 10 intermediários
            adicionar_botoes_em_pares(list(grupos_selecionados.items())[10:20])  # 10 intermediários

            # Adicionar os 10 últimos
            if len(buttons) >= 1:
                    markup.add(buttons[2])  # 1 botão na primeira linha
            adicionar_botoes_em_pares(list(grupos_selecionados.items())[20:])   # 10 últimos


            markup.add(
                InlineKeyboardButton('⚙ 𝗔𝗗𝗜𝗖𝗜𝗢𝗡𝗔𝗥 𝗚𝗥𝗨𝗣𝗢 🔗', url="https://t.me/BravusListBot")
            )

            # Envia a mensagem e armazena a resposta
            msg = bot.send_message(grupo_id, "Categoria Geral", reply_markup=markup, parse_mode='HTML')
            print(f"✅ Lista enviada para o grupo {grupo_id}.")
            
            # Salva os detalhes da mensagem enviada no banco de dados
            cursor.execute("""
                INSERT INTO listas_rastreadas (chat_id, mensagem_id, data_envio)
                VALUES (%s, %s, %s)
            """, (grupo_id, msg.message_id, datetime.datetime.now()))
            conn.commit()
            print(f"✅ Registro inserido na tabela ListaRastreada para o grupo {grupo_id}.")
        except Exception as e:

            print(f"❌ Erro ao enviar mensagem para o grupo {grupo_id}: {e}")

            # Fechar a conexão do banco
    cursor.close()
    conn.close()


# carregar_dados()
# lista_adulta()
# lista_geral()

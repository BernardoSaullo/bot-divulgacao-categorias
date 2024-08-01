import colorama
from colorama import Fore, Back, Style

# Inicializa o colorama


class Mensagens:
    colorama.init(autoreset=True)

    def EncerraAçao(self):
        print('='*30)
        print('AÇÃO ENCERRADO COM SUCESSO')
        print('='*30)

    # Função para imprimir uma mensagem de opcao_invalida
    def opcao_invalida(self):
        print('x'*30)
        print('        OPÇÃO INVALIDA           ')
        print('x'*30)

    # Função para imprimir uma mensagem de boas-vindas
    def boasvindas(self):
        print('='*30)
        print('-'*30,'\n')
        print('Seja Bem-Vindo\nEscolha uma das funções abaixo')
        print('-'*30,)
        print('='*30,'\n')


    # def bloco_nao_existente():
    #     print('x'*30)
    #     print('Este bloco não existe')
    #     print('x'*30)
    #     print('\nDigite novamente\n')

if __name__ == "__main__":
    c = Mensagens()
    c.boasvindas()
    
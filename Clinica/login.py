import stdiomask
from databases.run_sql import DatabaseManager
from classes.atendente import Atendente
from classes.paciente import Paciente
from classes.psicologo import Psicologo
# # Solicitar a senha do usuário e mascarar a entrada
# senha = stdiomask.getpass(prompt="Digite sua senha: ")

# # Exibir a senha digitada (apenas para fins de demonstração; não faça isso em um ambiente real)
# print("A senha digitada foi:", senha)



class Conta:
    def __init__(self):
     
        self.DB = DatabaseManager()


    def __verificar_senha(self,senha1,senha2):
        while not senha1 == senha2:
            print("As senhas precisão ser iguais ")
            senha1 = stdiomask.getpass(prompt="Digite sua senha: ", mask="*")
            senha2 = stdiomask.getpass(prompt="Confirme sua senha: ", mask="*")
            if senha1 == senha2:
                print("Senha passou")
                return senha1


    def __verificar_entrada(self,entrada):
        try:
            while True:
                if entrada.isdigit():
                    entrada = int(entrada)
                    if entrada == 1: # Quer dizer que ele já tem conta
                        entrada = True

                    elif entrada == 2:
                        entrada = False # Quer dizer que ele não tem conta
                    elif entrada == 0:
                        break
                    else:
                        print('Opção invalida')

                else:
                    print('Opção invalida')
            
        except:
            pass # cria exececão

    def criar_conta(self):

        self.entrada_criar_conta = int(input("""
[Criar Conta como]
                  
[1] Paciente
[2] Atendente
[3] Psicólogo                              
Digite sua opição: """))
            
        try:
            while True:
                if self.entrada_criar_conta == 1:
                    self.DB.conectar() 
                    print("Informe seus dados: ")
                    nome = input("Nome completo: ")
                    idade = input("Idade: ")
                    numero = input("Numero de Telefone: ")
                    cpf = input("CPF:")
                    endereco = input("Endereco: ")
                    print("Defina um nome de usuario, email e uma senha: ")
                    nome_usuario = input("Nome de Usúario")
                    email = input("Email: ")
                    senha = stdiomask.getpass(prompt="Digite sua senha: ", mask="*")
                    confirmar_senha = stdiomask.getpass(prompt="Confirme sua senha: ", mask="*")


                    senha_confirmada = self.__verificar_senha(senha,confirmar_senha)


                    paciente = Paciente(nome, idade ,numero ,cpf ,endereco ,nome_usuario ,email ,senha_confirmada)
                    self.DB.inserir(paciente)
                    self.DB.desconectar()
    
                    

                            

                elif self.entrada_criar_conta == 2:
                    self.DB.conectar()
                    print("Informe seus dados: ")
                    nome = input("Nome completo: ")
                    print("Defina um nome de usuario, email e uma senha: ")
                    nome_usuario = input("Nome de Usúario")
                    email = input("Email: ")
                    senha = stdiomask.getpass(prompt="Digite sua senha: ", mask="*")
                    confirmar_senha = stdiomask.getpass(prompt="Confirme sua senha: ", mask="*")

                    senha_confirmada = self.__verificar_senha(senha,confirmar_senha)


                    atendente = Atendente(nome, nome_usuario ,email ,senha_confirmada)
                    self.DB.inserir(atendente)
                    self.DB.desconectar()




                elif self.entrada_criar_conta == 3:
                    self.DB.conectar()
                    print("Informe seus dados: ")
                    nome = input("Nome completo: ")
                    especialidade = input("Especialidade: ")
                    print("Defina um nome de usuario, email e uma senha: ")
                    nome_usuario = input("Nome de Usúario")
                    email = input("Email: ")
                    senha = stdiomask.getpass(prompt="Digite sua senha: ", mask="*")
                    confirmar_senha = stdiomask.getpass(prompt="Confirme sua senha: ", mask="*")

                    senha_confirmada = self.__verificar_senha(senha,confirmar_senha)


                    psicologo = Psicologo(nome, especialidade ,nome_usuario ,email ,senha_confirmada)
                    self.DB.inserir(psicologo)
                    self.DB.desconectar()

        except:
            pass

    #     def fazer_login(self,entrada):
    #         try:

    #             if entrada:
    #                 self.entrada_criar_conta = int(input("""
    # [Criar Conta como]
                    
    # [1] Paciente
    # [2] Atendente
    # [3] Psicólogo                              
    # Digite sua opição: """))
                    
                
                



c = Conta()

c.criar_conta()


      




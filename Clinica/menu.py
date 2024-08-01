from databases.run_sql import DatabaseManager

class Opcioes:

    def op_atendente(self):
        print('''
(Atendente)
------------------------------------------
Escolha uma opção:

1  [Atendente]
2  [Consulta]
3  [Paciente]
4  [Pagamento]
5  [Psicólogo]
------------------------------------------
''')
        
    def op_psicologo(self):
        print('''
(Psicólogo)
------------------------------------------
Escolha uma opção:

1  [Prontuário]
2  [Consultas]
------------------------------------------
''')
        
    def op_paciente(self):
        print('''
(Paciente)
------------------------------------------

1  [Consulta]
2  [Pagamento]
------------------------------------------
''')
        


class Menu:
    def __init__(self,entrada: int) :
        
        self.databasemanager = DatabaseManager()
        self.opcioes = Opcioes()
        self.entrada = entrada
    def login(self):
        try:
            while True:
                if self.entrada.isdigit():
                    if self.entrada == 1: # Quer dizer que ele já tem conta
                        self.entrada = True
                    elif self.entrada == 2:
                        self.entrada = False # Quer dizer que ele não tem conta
                    elif self.entrada == 0:
                        break
                    else:
                        print('Opção invalida')

                else:
                    print('Opção invalida')
            
        except:
            pass # cria exececão

        
    




c = DatabaseManager()
cc = Menu(c)



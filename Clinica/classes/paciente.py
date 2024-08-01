from dataclasses import dataclass,fields

@dataclass
class Paciente:
    nome : str 
    idade: int
    numero: str
    cpf: str
    endereco: str
    nome_usuario: str
    email: str
    senha: str
    criado = None
    id = None
    



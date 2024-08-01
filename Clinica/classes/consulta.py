from dataclasses import dataclass,fields
from datetime import datetime


@dataclass
class Consulta:

    horario : int
    psicologo_id : int
    paciente_id : int
    status : str
    id = None


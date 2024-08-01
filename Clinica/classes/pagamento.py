from dataclasses import dataclass

@dataclass
class Pagamento:
    consulta = int
    status = str
    id = None



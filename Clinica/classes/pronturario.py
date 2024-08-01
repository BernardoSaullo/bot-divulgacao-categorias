from dataclasses import dataclass,fields

@dataclass
class Pronturario:
    paciente : int
    historico_clinico : str
    avaliacoes_psicologicas : str
    plano_terapeutico : str
    evolucao_sessoes : str
    anotacoes_encerramento : str
    id = None



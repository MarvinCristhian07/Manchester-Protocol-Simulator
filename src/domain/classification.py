import enum

class Classification(enum.Enum):
    '''
    Aqui eu defino as classificações de urgência do Protocolo de Manchester

    Cada membro possui três valores:
    1. A cor (representada por emoji)
    2. O nome da classificação
    3. Nível de prioridade, onde 0 é o mais urgente (vou usar números pra conseguir manipular melhor a urgência de cada paciente)
    '''

    RED     = ("🟥", "Emergência (atendimento imediato!)", 0)
    ORANGE  = ("🟧", "Muito urgente", 1)
    YELLOW  = ("🟨", "Urgente", 2)
    GREEN   = ("🟩", "Pouco urgente", 3)
    BLUE    = ("🟦", "Não urgente", 4)

    def __init__(self, color_emoji, description, priority_level):
        # Inicializador customizado para os membros da Enum
        self._color_emoji = color_emoji
        self._description = description
        self._priority_level = priority_level

    @property
    def color(self):
        # Retorna o emoji da cor
        return self._color_emoji
    
    @property
    def description(self):
        # Retorna o descrição da classificação
        return self._description
    @property
    def priority(self):
        # Retorna o nível de prioridade
        return self._priority_level
    
    @classmethod
    def get_by_priority(cls, level: int):
        # Método auxiliar para encontrar uma classificação pelo nível de prioridade
        for Classification in cls:
            if Classification.priority == level:
                return Classification
        raise ValueError(f"Nenhum nível de prioridade correspondente a '{level}'")
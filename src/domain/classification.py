import enum

class Classification(enum.Enum):
    '''
    Aqui eu defino as classificações de urgência do Protocolo de Manchester

    Cada membro possui três valores:
    1. A cor (representada por emoji)
    2. O nome da classificação
    3. Nível de prioridade, onde 0 é o mais urgente (vou usar números pra conseguir manipular melhor a urgência de cada paciente)
    '''

    RED    = ("🟥", "Emergência (atendimento imediato)", 0, "#E53E3E")
    ORANGE = ("🟧", "Muito urgente", 1, "#DD6B20")
    YELLOW = ("🟨", "Urgente", 2, "#D69E2E")
    GREEN  = ("🟩", "Pouco urgente", 3, "#38A169")
    BLUE   = ("🟦", "Não urgente", 4, "#3182CE")

    def __init__(self, color_emoji, description, priority_level, hex_color):
        # Inicializador customizado para os membros da Enum
        self._color_emoji = color_emoji
        self._description = description
        self._priority_level = priority_level
        self._hex_color = hex_color

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
    
    @property
    def hex_color(self):
        # Retorna a cor hexadecimal
        return self._hex_color
    
    @classmethod
    def get_by_priority(cls, level: int):
        # Método auxiliar para encontrar uma classificação pelo nível de prioridade
        for classification_member in cls:
            if classification_member.priority == level:
                return classification_member
        raise ValueError(f"Nenhum nível de prioridade correspondente a '{level}'")

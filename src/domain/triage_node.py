from typing import Optional, Self
from src.domain.classification import Classification

class NodoArvore:
    '''
    Representa um nó na árvore de decisão da triagem (Decision Tree).

    Um nó é mutuamente exclusivo:
    - Ou é um nó de pergunta (interno) com uma 'question' e dois filhos
    - Ou é um nó folha (terminal) com uma 'classification' final
    '''

    def __init__(self,
                 question: Optional[str] = None,
                 classification: Optional[Classification] = None,
                 yes_child: Optional[Self] = None,
                 no_child: Optional[Self] = None):
        # Construtor da árvore, valida a lógica de negócio do nó
        
        # 1. Validação da lógica exclusiva (pergunta ou folha)
        if (question and classification):
            raise ValueError("Um nó não pode ser uma pergunta e uma classificação ao mesmo tempo.")
        
        if not question and not classification:
            raise ValueError("Um nó deve ser ou uma pergunta (interna) ou uma classificação (folha).")
        
        # 2. Validação de Nó de pergunta
        if question:
            if not yes_child or not no_child:
                raise ValueError(f"Nó de pergunta ('{question}') deve ter ambos os filhos (yes_child e no_child).")
            
            if not isinstance(yes_child, NodoArvore) or not isinstance(no_child, NodoArvore):
                raise ValueError("Os filhos (yes_child/no_child) devem ser instâncias de NodoArvore.")
            
        # 3. Validação de Nó de folha
        if classification:
            if yes_child or no_child:
                raise ValueError("Nó folha (classificação) não pode ter filhos.")
            
            if not isinstance(classification, Classification):
                raise TypeError("A classificação deve ser uma instância da Enum Classification.")
            
        self.question = question
        self.classification = classification
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self) -> bool:
        # Método auxiliar limpo para verificar se este nó é uma folha
        return self.classification is not None
    
    def __str__(self) -> str:
        # Retorna uma representação legível do nó
        if self.is_leaf():
            return f"[Folha: {self.classification.color} {self.classification.name}]"
        else:
            return f"[Pergunta: '{self.question}']"
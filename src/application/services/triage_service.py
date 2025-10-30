from src.domain.triage_node import NodoArvore
from src.domain.classification import Classification
from src.infrastructure.triage_builder import montar_arvore
from typing import Optional

def _ask_yes_no(prompt: str) -> bool:
    '''
    Função auxiliar privada para o console
    '''
    while True:
        try:
            answer = input(f"\n[PERGUNTA] {prompt} (S/N): ").strip().upper()
            if answer == 'S' or answer == 'SIM':
                return True
            elif answer == 'N' or answer == 'NAO' or answer == 'NÃO':
                return False
            else:
                print(f"ERRO: Resposta '{answer}' inválida. Por favor, digite 'S' para Sim ou 'N' para Não.")
        except KeyboardInterrupt:
            print("\nTriagem interrompida.")
            raise

def triagem_console(root_node: NodoArvore) -> Classification:
    if not root_node or not isinstance(root_node, NodoArvore):
        raise ValueError("A árvore de triagem (root_node) é inválida.")
    
    print("--- Iniciando Triagem (Modo Console) ---")
    current_node = root_node
    
    try:
        while not current_node.is_leaf():
            answer_is_yes = _ask_yes_no(current_node.question)
            current_node = current_node.yes_child if answer_is_yes else current_node.no_child
            
        final_classification = current_node.classification
        print("--- Triagem Concluída ---")
        print(f"Resultado: {final_classification.color} {final_classification.description}")
        return final_classification
    except KeyboardInterrupt:
        raise SystemError("Triagem interrompida pelo usuário.")


class TriageNavigator:
    '''
    Classe controlável pela GUI para navegar na árvore de decisão
    Ela mantém o estado da triagem
    '''
    def __init__(self, root_node: NodoArvore):
        if not root_node or not isinstance(root_node, NodoArvore):
            raise ValueError("A árvore de triagem (root_node) é inválida.")
        self.root_node = root_node
        self.current_node = root_node

    def get_current_question(self) -> Optional[str]:
        '''Retorna a pergunta atual, ou None se a triagem terminou'''
        if self.is_finished():
            return None
        return self.current_node.question

    def navigate(self, answer_is_yes: bool):
        '''Avança na árvore com base na resposta'''
        if self.is_finished():
            return
            
        if answer_is_yes:
            self.current_node = self.current_node.yes_child
        else:
            self.current_node = self.current_node.no_child
            
    def is_finished(self) -> bool:
        ''' Verifica se a triagem chegou a uma folha (classificação)'''
        return self.current_node.is_leaf()

    def get_final_classification(self) -> Optional[Classification]:
        ''' Retorna a classificação final, ou None se não terminou '''
        if self.is_finished():
            return self.current_node.classification
        return None
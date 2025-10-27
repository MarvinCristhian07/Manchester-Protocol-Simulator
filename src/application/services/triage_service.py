from src.domain.triage_node import NodoArvore
from src.domain.classification import Classification

def _ask_yes_no(prompt: str) -> bool:
    '''
    Função auxiliar privada para fazer pergunta de Sim/Não ao usuário

    Valida a entrada e continua perguntando até receber 'S' ou 'N'

    Args:
        prompt (str): A pergunta a ser exibida.

    Returns:
        bool: True se o usuário digitar 'S' ou False se for 'N'
    '''
    while True:
        try:
            # Só pra garantir que a pergunta seja bem formatada
            answer = input(f"\n[PERGUNTA] {prompt} (S/N): ").strip().upper()

            if answer == 'S' or answer == "SIM":
                return True
            elif answer == 'N' or answer == "NÃO":
                return False
            else:
                print(f"ERRO: Resposta '{answer}' inválida. Por favor, digite 'S' para Sim ou 'N' para Não.")
        
        except KeyboardInterrupt:
            print("\nTriagem interrompida pelo usuário.")
            raise
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            raise SystemError("Falha na entrada de dados.")

def triagem(root_node: NodoArvore) -> Classification:
    '''
    Executa o processo de triagem percorrendo a árvore de decisão. 
    Faz as perguntas ao usuário e navega na árvore com base nas respostas
    'Sim' ou 'Não" até chegar a um nó folha (classificação).

    Args:
        root_node (NodoArvore): O nó raiz da árvore

    Returns:
        Classification: A classificação final (vermelho, laranja....)

    Raises:
        ValueError: Se a árvore fornecida for nula ouu inválida
    '''
    if not root_node or not isinstance(root_node, NodoArvore):
        raise ValueError("A árvore de triagem (root_node) é inválida ou não foi fornecida.")
    
    print("--- Iniciando Triagem ---")

    current_node = root_node

    # Vai navegar na árvore enquanto o nó atual não for uma folha
    while not current_node.is_leaf():
        # Função auxiliar cuida da validação da entrada
        answer_is_yes = _ask_yes_no(current_node.question)

        if answer_is_yes:
            current_node = current_node.yes_child
        else:
            current_node = current_node.no_child

    # Ao sair do loop, current_node é uma folha (ou seja, chegou à uma classificação!)
    final_classification = current_node.classification

    print("--- Triagem Concluída ---")
    print(f"Resultado: {final_classification.color} {final_classification.description}")

    return final_classification
from src.domain.triage_node import NodoArvore
from src.domain.classification import Classification

def montar_arvore() -> NodoArvore:
    '''
    Construir e retornar o nó raiz da árvore de decisão de triagem

    Returns:
        NodoArvore: O nó raiz da árvore de Triagem

    Raises:
        SystemError: Se houver um erro de programação na montagem da árvore
    '''

    print("[Builder] Iniciando montagem da árvore de decisão...")

    try:
        # Nível 4 → Folhas (final da árvore)
        leaf_red       = NodoArvore(classification=Classification.RED)
        leaf_orange    = NodoArvore(classification=Classification.ORANGE)
        leaf_yellow    = NodoArvore(classification=Classification.YELLOW)
        leaf_greem     = NodoArvore(classification=Classification.GREEN)
        leaf_blue      = NodoArvore(classification=Classification.BLUE)

        # Nível 3 → Definir o caminho para o verde ou azul
        node_administrativo = NodoArvore(
            question="A visita é para renovação de receita, atestado ou consulta de rotina?",
            yes_child=leaf_blue,
            no_child=leaf_greem
        )

        # Nível 2 → Diferencia o amarelo do verde/azul
        node_sintomas_moderados = NodoArvore(
            question="Sintomas moderados (ex: febre alta, vômito persistente, dor moderada?)",
            yes_child=leaf_yellow,
            no_child=node_administrativo
        )

        # Nível 1 → Diferencia laranja de amarelo/verde/azul
        node_risco_imediato = NodoArvore(
            question="Sinais de alerta (ex: dor no peito, sangramento severo, confusão mental?)",
            yes_child=leaf_orange,
            no_child=node_sintomas_moderados
        )

        # Nível 0 (raiz) → Pergunta mais crítica que será usada para definir o vermelho
        root_node = NodoArvore(
            question="Paciente apresenta parada respiratória/cardíaca ou está inconsciente?",
            yes_child=leaf_red,
            no_child=node_risco_imediato
        )

        print("[Builder] Árvore de 5 níveis montada com sucesso!")
        return root_node
    
    except (ValueError, TypeError) as e:
        # Erro de programação na definição da árvore
        error_message = f"ERRO CRÍTICO ao montar a árvore de triagem: {e}"
        print(error_message)
        raise SystemError(error_message) from e
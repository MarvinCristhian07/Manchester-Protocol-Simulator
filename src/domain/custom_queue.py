from collections import deque
from typing import Any, Optional

class EmptyQueueError(Exception):
    # Exceção customizada para fila vazia
    def __init__(self, message="A fila está vazia. Não é possível desinfileirar."):
        self.message = message
        super().__init__(self.message)

class Fila:
    '''
    Aqui vou implementar uma estrutura de dados de Fila (FIFO: First-In, First-Out) utilizando
    collections.deque para operações otimizadas 0(1).
    '''

    def __init__(self):
        # Inicializa a fila interna como um deque vazio
        self._queue = deque()

    def enqueue(self, item: Any):
        '''
        Adiciona um item ao final da fila

        Args:
            item (Any): O item a ser adicionado (ex: um paciente)
        '''
        if item is None:
            raise ValueError("Não é possível adicionar um item 'None'.")
        
        self._queue.append(item)
        print(f"[Fila] Item '{item}' enfileirado.")

    def dequeue(self) -> Optional[Any]:
        '''
        Remove e retorna o item do início da fila

        Returns:
            Any: O item do início da fila

        Raises:
            EmptyQueueError: Se a fila estiver vazia
        '''
        try:
            item = self._queue.popleft()
            print(f"[Fila] Item '{item}' desenfileirado.")
            return item
        except IndexError:
            raise EmptyQueueError()
        
    def is_empty(self) -> bool:
        # Verifica se a fila está vazia
        return len(self._queue) == 0
    
    def size(self) -> int:
        # Retorna o número de itens na fila
        return len(self._queue)
    
    def __len__(self) -> int:
        # Permite o uso da função nativa len() na fila
        return self.size()
    
    def __str__(self) -> str:
        # Retorna uma representação em string da fila
        return f"Fila (Início -> Fim): {list(self._queue)}"
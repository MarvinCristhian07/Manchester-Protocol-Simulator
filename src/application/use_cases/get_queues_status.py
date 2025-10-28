from typing import Dict
from src.domain.classification import Classification
from src.application.interfaces.i_queue_repository import IQueueRepository

class GetQueuesStatusUseCases:
    '''
    Caso de Uso para obter o status (tamanho) de todas as filas
    
    Busca no repositório a contagem de pacientes em cada fila
    '''

    def __init__(self, queue_repo: IQueueRepository):
        '''
        Inicializa o caso de uso com suas dependências
        
        Args:
            queue_repo (IQueueRepository): Uma implementação do repositório 
                                           de filas
        '''
        if not isinstance(queue_repo, IQueueRepository):
            raise TypeError("O repositório (queue_repo) deve implementar a interface IQueueRepository")
            
        self.queue_repo = queue_repo
        print("[UseCase Init] Caso de Uso 'GetQueuesStatus' pronto.")

    def execute(self) -> Dict[Classification, int]:
        '''
        Executa o fluxo de obtenção do status das filas'
        
        Returns:
            Dict[Classification, int]: Um dicionário onde a chave é a
                                       classificação e o valor é o 
                                       número de pacientes na fila
                                       
        Raises:
            SystemError: Se ocorrer uma falha inesperada no repositório
        '''
        print("\n--- Iniciando Caso de Uso: Obter Status das Filas ---")
        
        try:
            # 1. Pedir ao Repositório (via Interface)
            status_dict = self.queue_repo.get_status()
            
            print("[UseCase] Status das filas obtido com sucesso.")
            
            # 2. Retornar para a Camada de Apresentação
            return status_dict

        except Exception as e_repo:
            # Captura qualquer erro inesperado vindo do repositório
            print(f"[UseCase] Erro ao tentar obter o status das filas: {e_repo}")
            raise SystemError("Falha ao processar a solicitação de status.") from e_repo
from typing import Optional
from src.domain.patient import Patient
from src.application.interfaces.i_queue_repository import IQueueRepository

class CallNextPatientUseCase:
    '''
    Caso de Uso para chamar (remover) o próximo paciente
    
    Orquestra a obtenção do paciente da fila de maior prioridade
    disponível através do repositório
    '''
    def __init__(self, queue_repo: IQueueRepository):
        '''
        Inicializa o caso de uso com suas dependências
        
        Args:
            queue_repo (IQueueRepository): Uma implementação do repositório 
                                           de filas
        '''
        if not isinstance(queue_repo, IQueueRepository):
            raise TypeError("O repositório (queue_repo) deve implementar a interface IQueueRepository.")
        
        self.queue_repo = queue_repo
        print("[UseCase Init] Caso de Uso 'CallNextPatient' pronto.")
        
    def execute(self) -> Optional[Patient]:
        '''
        Executa o fluxo de chamada do próximo paciente
        
        Pede ao repositório o próximo paciente. O repositório já
        contém a lógica de prioridade (Vermelho -> Azul)
        
        Returns:
            Optional[Patient]: O paciente que foi chamado (e removido
                               da fila), ou None se todas as filas
                               estiverem vazias
                               
        Raises:
            SystemError: Se ocorrer uma falha inesperada no repositório
        '''
        print("\n--- Iniciando Caso de Uso: Chamar Próximo Paciente ---")
        
        try:
            patient = self.queue_repo.get_next_patient()
            
            if patient:
                print(f"[UseCase] Paciente '{patient.name}' encontrado e removido da fila.")
            else:
                print("[UseCase] Todas as filas estão vazias. Nenhum paciente para chamar.")
                
            return patient
        
        except Exception as e_repo:
            print(f"[UseCase] Erro ao tentar obter o próximo paciente: {e_repo}")
            raise SystemError("Falha ao processar a chamada do paciente.") from e_repo
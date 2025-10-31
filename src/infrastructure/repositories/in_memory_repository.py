from typing import Dict, Optional
from src.domain.classification import Classification
from src.domain.custom_queue import Fila, EmptyQueueError
from src.domain.patient import Patient
from src.application.interfaces.i_queue_repository import IQueueRepository

class InMemoryQueueRepository(IQueueRepository):
    '''
    Implementação em memória da interface IQueueRepository
    
    Gerencia 5 instâncias da classe Fila, uma para cada níveL de classificação do Protocolo de Manchester
    '''

    def __init__(self):
        # Inicializa o repositório criando 5 linhas vazias
        self.queues: Dict[Classification, Fila] = {
            cls: Fila() for cls in Classification
        }
        print("[Repo] Repositório em memória inicializado com 5 filas.")

    def add_patient(self, patient: Patient, classification: Classification):
        '''
        Adiciona um paciente à fila correta
        
        Args:
            patient (Patient): O objeto do paciente
            classification (Classification): A classificação (cor) da fila
            
        Raises:
            KeyError: Se a classificação fornecida não for válida
        '''
        try:
            queue = self.queues[classification]
            queue.enqueue(patient)
            print(f"[Repo] Paciente '{patient.name}' adicionado à fila {classification.name}.")
        except KeyError:
            # Erro de programação: A classificação não existe mais no dict
            raise KeyError(f"Classificação '{classification}' inválida. Não existe fila para ela.")
        except ValueError as e:
            # Erro vindo do enqueue, ex: patient: None
            print(f"Erro ao enfileirar: {e}")
            raise
          
    def get_next_patient(self) -> Optional[Patient]:
        '''
        Busca o próximo paciente na ordem de prioridade (Vermelho -> Azul)
        
        Returns:
            Optional[Patient]: O paciente encontrado, ou None se todas as
                               filas estiverem vazias
        '''
        
        for priority_level in sorted([cls.priority for cls in Classification]):
            try:
                classification = Classification.get_by_priority(priority_level)
                queue = self.queues[classification]
                
                if not queue.is_empty():
                    # Fila mais prioritária com pacientes encontrada
                    patient = queue.dequeue()
                    print(f"[Repo] Chamando paciente '{patient.name}' da fila {classification.name}.")
                    return patient
                    
            except EmptyQueueError:
                continue
            except KeyError:
                # Erro de programação, ex: prioridade 5 não existe
                print(f"Erro: Nível de prioridade {priority_level} não encontrado.")
                continue # Pula para a próxima prioridade

        # Se o loop terminar, todas as filas estão vazias
        print("[Repo] Todas as filas estão vazias.")
        return None

    def get_status(self) -> Dict[Classification, int]:
        '''
        Retorna o tamanho de cada fila.
        
        Returns:
            Dict[Classification, int]: Dicionário (Classificação -> tamanho).
        '''

        status = {
            classification: queue.size() 
            for classification, queue in self.queues.items()
        }
        return status

from abc import ABC, abstractmethod
from typing import Optional, Dict
from src.domain.patient import Patient
from src.domain.classification import Classification

class IQueueRepository(ABC):
    '''
    Essa é a interface que define as operações obrigatórias para um repositório de gerenciamento de filas de pacientes
    Com isso, qualquer classe que implementar essa interface deve fornecer a lógica para os métodos a seguir
    '''

    @abstractmethod
    def add_patient(self, patient: Patient, classification: Classification):
        '''
        Adiciona um paciente na fila correspondente à sua classificação

        Args:
            patient (Patient): O objeto do paciente
            classification (Classification): A classificação (cor) da fila
        '''
        pass

    @abstractmethod
    def get_next_patient(self) -> Optional[Patient]:
        '''
        Remove e retorna o próximo paciente da fila de maior prioridade
        
        A ordem de prioridade deve ser: Vermelho → Laranja → Amarelo → Verde → Azul
        
        Returns:
            Optional[Patient]: O objeto do paciente, ou None se todas as filas estiverem vazias
        '''
        pass
     
    @abstractmethod
    def get_status(self) -> Dict[Classification, int]:
        '''
        Retorna o tamanho atual de cada uma das 5 filas
        
        Returns:
            Dict[Classification, int]: Um dicionário onde a chave é a
                                       classificação e o valor é o 
                                       número de pacientes na fila
        '''     
        pass

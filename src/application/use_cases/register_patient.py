from src.domain.patient import Patient
from src.domain.classification import Classification
from src.application.interfaces.i_queue_repository import IQueueRepository

from src.infrastructure.repositories.in_memory_repository import InMemoryQueueRepository
from src.infrastructure.triage_builder import montar_arvore

class RegisterPatientUseCase:
    '''
    Caso de Uso para registrar um paciente já classificado
    
    Responsável apenas por validar e adicionar o paciente ao
    repositório na fila correta
    '''

    def __init__(self, queue_repo: IQueueRepository):
        '''
        Inicializa o caso de uso
        
        Args:
            queue_repo (IQueueRepository): Implementação do repositório
        '''
        if not isinstance(queue_repo, IQueueRepository):
            raise TypeError("O repositório (queue_repo) deve implementar a interface IQueueRepository")
            
        self.queue_repo = queue_repo
        print("[UseCase Init] Caso de Uso 'RegisterPatient' pronto (simplificado).")

    def execute(self, patient: Patient, classification: Classification):
        '''
        Executa o fluxo de cadastro do paciente
        
        Args:
            patient (Patient): O objeto Paciente
            classification (Classification): A classificação final
                                            
        Raises:
            ValueError: Se o paciente ou classificação forem inválidos
            SystemError: Se o salvamento no repo falhar
        '''
        print(f"\n--- Iniciando Caso de Uso: Registrar Paciente '{patient.name}' ---")
        
        try:
            # Validação
            if not patient or not isinstance(patient, Patient):
                raise ValueError("Objeto 'Patient' inválido.")
            if not classification or not isinstance(classification, Classification):
                raise ValueError("Objeto 'Classification' inválido.")

            # Adicionar à Fila (Infraestrutura via Interface)
            self.queue_repo.add_patient(patient, classification)
            print("[UseCase] Paciente adicionado à fila com sucesso.")
            
        except (KeyError, ValueError) as e_repo:
            print(f"[UseCase] Erro ao adicionar paciente ao repositório: {e_repo}")
            raise SystemError("Falha ao salvar paciente na fila.") from e_repo
        
        # Retorna True em sucesso (ou nada)
        return True
from typing import Tuple
from src.domain.patient import Patient
from src.domain.classification import Classification
from src.domain.triage_node import NodoArvore
from src.application.interfaces.i_queue_repository import IQueueRepository
from src.application.services.triage_service import triagem

class RegisterPatientUseCase:
    def __init__(self, queue_repo: IQueueRepository, triage_tree_root: NodoArvore):
        '''
        Inicializa o caso de uso com suas dependências (Injeção de Dependência)
        
        Args:
            queue_repo (IQueueRepository): Uma implementação do repositório 
                                           de filas
            triage_tree_root (NodoArvore): O nó raiz da árvore de triagem 
                                            já montada
        '''
        if not isinstance(queue_repo, IQueueRepository):
            raise TypeError("O repositório (queue_repo) deve implementar a interface IQueueRepository")
        if not isinstance(triage_tree_root, NodoArvore):
            raise TypeError("A raiz da árvore (triage_tree_root) deve ser um NodoArvore")
        
        self.queue_repo = queue_repo
        self.triage_tree_root = triage_tree_root
        print("[UseCase Init] Caso de Uso 'RegisterPatient' pronto.")
        
    def execute(self, patient_name: str) -> Tuple[Patient, Classification]:
        '''
        Executa o fluxo de cadastro do paciente
        
        Args:
            patient_name (str): O nome do paciente (fornecido pela UI)
            
        Returns:
            Tuple[Patient, Classification]: O paciente criado e sua 
                                            classificação final
                                            
        Raises:
            ValueError: Se o nome do paciente for inválido (vindo do Domain)
            SystemError: Se a triagem ou o salvamento no repo falharem
        '''
        print(f"\n--- Iniciando Caso de Uso: Registrar Paciente '{patient_name}' ---")
        
        try:
            patient = Patient(name=patient_name)
            print(f"[UseCase] Paciente '{patient_name}' criado com ID: {patient.id}.")
            
        except ValueError as e_domain:
            print(f"[UseCase] Erro de validação: {e_domain}")
            raise
        
        try:
            final_classification = triagem(self.triage_tree_root)
            print(f"[UseCase] Triagem concluída. Resultado: {final_classification.name}")
            
        except Exception as e_triage:
            print(f"[UseCase] Erro crítico durante a triagem: {e_triage}")
            raise SystemError("A triagem foi interrompida ou falhou.") from e_triage
        
        try:
            self.queue_repo.add_patient(patient, final_classification)
            print("[UseCase] Paciente adicionado à fila com sucesso.")
            
        except (KeyError, ValueError) as e_repo:
            print(f"[UseCase] Erro ao adicionar paciente ao repositório: {e_repo}")
            raise SystemError("Falha ao salvar paciente na fila.") from e_repo
        
        return (patient, final_classification)
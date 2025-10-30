import sys
import os
from typing import Dict, Tuple

# --- Bloco de correção de Path (IMPORTANTE) ---
current_file_path = os.path.abspath(__file__)
console_dir = os.path.dirname(current_file_path)
presentation_dir = os.path.dirname(console_dir)
src_dir = os.path.dirname(presentation_dir)
project_root = os.path.dirname(src_dir)

if project_root not in sys.path:
    sys.path.append(project_root)
# --- Fim do Bloco de correção de Path ---

from src.domain.patient import Patient
from src.domain.classification import Classification
from src.domain.triage_node import NodoArvore
from src.infrastructure.triage_builder import montar_arvore
from src.infrastructure.repositories.in_memory_repository import InMemoryQueueRepository

# --- CORREÇÃO 1: Importações ---
# Corrigido o 's' extra em GetQueuesStatusUseCase
# Corrigido o serviço de triagem para usar a versão de console
from src.application.use_cases.register_patient import RegisterPatientUseCase
from src.application.use_cases.call_next_patient import CallNextPatientUseCase
from src.application.use_cases.get_queues_status import GetQueuesStatusUseCase
from src.application.services.triage_service import triagem_console # MUDANÇA AQUI


def _show_menu():
    print("\n" + "="*40)
    print(" 🏥 SIMULADOR DE PROTOCOLO MANCHESTER 🏥")
    print("="*40)
    print("1 - Cadastrar novo paciente (iniciar triagem)")
    print("2 - Chamar próximo paciente (por prioridade)")
    print("3 - Mostrar status das filas")
    print("0 - Sair")

def _handle_register_patient(use_case: RegisterPatientUseCase, triage_tree: NodoArvore):
    """
    Handler ATUALIZADO para o Caso de Uso 1 (Console).
    Agora ele orquestra a criação do paciente e a triagem_console.
    """
    print("\n[Opção 1: Cadastrar Paciente]")
    try:
        name = input("Digite o nome completo do paciente: ").strip()
        
        # --- LÓGICA ATUALIZADA ---
        # 1. A UI (console) cria o paciente
        patient = Patient(name=name)
        
        # 2. A UI (console) executa a triagem específica do console
        classification = triagem_console(triage_tree)
        
        # 3. A UI (console) chama o caso de uso SIMPLIFICADO para salvar
        use_case.execute(patient, classification)
        # --- FIM DA LÓGICA ---
        
        print("\n[CADASTRO CONCLUÍDO]")
        print(f"Paciente: {patient.name}")
        print(f"Classificação: {classification.color} {classification.description}")
        
    except ValueError as e:
        print(f"\nERRO DE VALIDAÇÃO: {e}")
    except SystemError as e:
        print(f"\nERRO NO SISTEMA: {e}")
    except KeyboardInterrupt:
        print("\nCadastro interrompido pelo usuário.")
        
def _handle_call_patient(use_case: CallNextPatientUseCase):
    print("\n[Opção 2: Chamar Próximo Paciente]")
    try:
        patient = use_case.execute()
        
        if patient:
            print(f"\nPróximo paciente a ser atendido:")
            print(f"==> {patient.name.upper()} <==")
        else:
            print("\nTodas as filas estão vazias. Nenhum paciente para chamar.")
            
    except SystemError as e:
        print(f"\nERRO NO SISTEMA: {e}")
        
def _handle_show_status(use_case: GetQueuesStatusUseCase): # <-- CORREÇÃO 2: 's' removido
    print("\n[Opção 3: Status das Filas]")
    try:
        status_dict = use_case.execute()
        
        sorted_status = sorted(status_dict.items(), key=lambda item: item[0].priority)
        
        print("-" * 35)
        print(" FILA           | PACIENTES")
        print("-" * 35)
        total = 0
        for classification, size in sorted_status:
            print(f" {classification.color} {classification.name:<15} | {size}")
            total += size
        print("-" * 35)
        print(f" TOTAL DE PACIENTES: {total}")
    
    except SystemError as e:
        print(f"\nERRO NO SISTEMA: {e}")
        
def setup_application() -> Tuple[RegisterPatientUseCase, CallNextPatientUseCase, GetQueuesStatusUseCase, NodoArvore]:
    """
    Função de setup ATUALIZADA.
    - Corrige o 's' extra em GetQueuesStatusUseCase.
    - Corrige o type hint de retorno para usar Tuple[...].
    - Não injeta mais a árvore no RegisterPatientUseCase.
    - Retorna a árvore para o 'main' usar.
    """
    print("Inicializando o Manchester Protocol Simulator...")
    
    try:
        print("[Setup] Montando árvore de triagem...")
        triage_tree = montar_arvore()
        
        print("[Setup] Criando repositório de filas em memória...")
        queue_repo = InMemoryQueueRepository()
        
        print("[Setup] Injetando dependências nos casos de uso...")
        
        # --- INJEÇÃO ATUALIZADA ---
        # RegisterPatientUseCase não precisa mais da árvore
        register_use_case = RegisterPatientUseCase(queue_repo) 
        call_use_case = CallNextPatientUseCase(queue_repo)
        status_use_case = GetQueuesStatusUseCase(queue_repo) # <-- CORREÇÃO 3: 's' removido
        
        print("Sistema pronto para operar.\n")
        
        # --- RETORNO ATUALIZADO ---
        # Retorna a árvore para o 'main' poder passá-la para o handler
        return register_use_case, call_use_case, status_use_case, triage_tree
    
    except SystemError as e:
        print(f"\n[ERRO CRÍTICO NA INICIALIZAÇÃO]")
        print(f"O sistema não pode iniciar: {e}")
        return None, None, None, None # type: ignore
    except Exception as e:
        print(f"\n[ERRO DESCONHECIDO NA INICIALIZAÇÃO]: {e}")
        return None, None, None, None # type: ignore
        
def main():
    # --- CHAMADA ATUALIZADA ---
    # Agora recebe 4 itens
    register_uc, call_uc, status_uc, triage_tree = setup_application()
    
    if not all([register_uc, call_uc, status_uc, triage_tree]):
        print("Encerrando aplicação devido a erro no setup.")
        return
    
    while True:
        _show_menu()
        
        try:
            choice_str = input("\nEscolha uma opção (1, 2, 3 ou 0): ").strip()
            
            if not choice_str.isdigit():
                print("\nERRO: Por favor, digite apenas números.")
                continue
            
            choice = int(choice_str)
            print("-" * 35)
            
            if choice == 1:
                # --- CHAMADA ATUALIZADA ---
                # Passa a árvore para o handler
                _handle_register_patient(register_uc, triage_tree)
            elif choice == 2:
                _handle_call_patient(call_uc)
            elif choice == 3:
                _handle_show_status(status_uc)
            elif choice == 0:
                print("\nEncerrando o sistema. Até logo!")
                break
            
            else:
                print(f"\nOpção '{choice}' inválida. Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n\nOperação interrompida pelo usuário. Encerrando o sistema.")
            break
        except Exception as e:
            print(f"\nERRO INESPERADO NO LOOP PRINCIPAL: {e}")
            print("Tentando continuar a execução...")
            
        print("\nPressione ENTER para continuar...")
        input()
        
if __name__ == "__main__":
    main()
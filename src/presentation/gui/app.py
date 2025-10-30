# --- Bloco de correção de Path (IMPORTANTE) ---
import sys
import os
from typing import Tuple, Optional

current_file_path = os.path.abspath(__file__)
gui_dir = os.path.dirname(current_file_path)
presentation_dir = os.path.dirname(gui_dir)
src_dir = os.path.dirname(presentation_dir)
project_root = os.path.dirname(src_dir)

if project_root not in sys.path:
    sys.path.append(project_root)
# --- Fim do Bloco de correção de Path ---


# --- Imports da Aplicação ---
import customtkinter

# Importações para o Setup (O "Mundo Real")
from src.infrastructure.triage_builder import montar_arvore
from src.infrastructure.repositories.in_memory_repository import InMemoryQueueRepository

# Importações dos Casos de Uso
from src.application.use_cases.register_patient import RegisterPatientUseCase
from src.application.use_cases.call_next_patient import CallNextPatientUseCase
from src.application.use_cases.get_queues_status import GetQueuesStatusUseCases

# Importações de Tipos e Janelas
from src.domain.triage_node import NodoArvore
from src.presentation.gui.triage_window import TriageWindow
from src.presentation.gui.status_window import StatusWindow
from src.presentation.gui.call_result_window import CallResultWindow


# --- Configurações do CustomTkinter ---
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    """
    Classe principal da aplicação GUI (Interface Gráfica).
    Herda de CTk, que é a janela principal.
    """
    
    def __init__(self, 
                 register_uc: RegisterPatientUseCase, 
                 call_uc: CallNextPatientUseCase, 
                 status_uc: GetQueuesStatusUseCases,
                 triage_tree: NodoArvore): # <-- Recebe a árvore
        
        super().__init__()

        # 1. Armazena os casos de uso (injeção de dependência)
        self.register_use_case = register_uc
        self.call_use_case = call_uc
        self.status_use_case = status_uc
        self.triage_tree = triage_tree # <-- Armazena a árvore

        # Armazena a referência da janela de triagem
        self.triage_window: Optional[TriageWindow] = None
        self.status_window: Optional[StatusWindow] = None
        self.call_window: Optional[CallResultWindow] = None

        # 2. Configura a janela principal
        self.title("Manchester Protocol Simulator (GUI)")
        self.geometry("500x350")
        self.minsize(400, 300)

        # 3. Cria os widgets (componentes da tela)
        self.setup_ui()

    def setup_ui(self):
        """Cria e posiciona os widgets na janela."""
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = customtkinter.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1) 

        title_label = customtkinter.CTkLabel(
            main_frame, 
            text="Menu Principal", 
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=30, pady=(20, 20))

        register_button = customtkinter.CTkButton(
            main_frame,
            text="1. Cadastrar Paciente (Iniciar Triagem)",
            font=customtkinter.CTkFont(size=14),
            height=40,
            command=self.open_register_window # <-- ATUALIZADO
        )
        register_button.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

        call_button = customtkinter.CTkButton(
            main_frame,
            text="2. Chamar Próximo Paciente",
            font=customtkinter.CTkFont(size=14),
            height=40,
            command=self.call_next_patient
        )
        call_button.grid(row=2, column=0, padx=30, pady=10, sticky="ew")

        status_button = customtkinter.CTkButton(
            main_frame,
            text="3. Mostrar Status das Filas",
            font=customtkinter.CTkFont(size=14),
            height=40,
            command=self.show_status_window
        )
        status_button.grid(row=3, column=0, padx=30, pady=(10, 20), sticky="ew")
        
        exit_button = customtkinter.CTkButton(
            main_frame,
            text="0. Sair",
            font=customtkinter.CTkFont(size=14),
            height=40,
            command=self.quit_app, # <-- Nova função
            # Cores para "destruir" (Vermelho escuro/claro)
            fg_color=("#F56565", "#C53030"),
            hover_color=("#E53E3E", "#9B2C2C")
        )
        exit_button.grid(row=4, column=0, padx=30, pady=(10, 20), sticky="ew")

    # --- Funções de Callback (Ações dos Botões) ---
    
    def open_register_window(self):
        """
        Ação para o botão 'Cadastrar'.
        Cria a janela de triagem (Toplevel), passando as dependências.
        """
        print("[GUI] Clicou em 'Cadastrar'.")
        
        # Verifica se a janela já não está aberta
        if self.triage_window is None or not self.triage_window.winfo_exists():
            # Cria a nova janela, passando as dependências
            self.triage_window = TriageWindow(
                master=self, 
                register_uc=self.register_use_case,
                triage_tree=self.triage_tree # <-- Passa a árvore
            )
            self.triage_window.grab_set() # Foca na nova janela
        else:
            self.triage_window.focus() # Foca se já existir

    def call_next_patient(self):
        """Ação para o botão 'Chamar'."""
        try:
            # 1. Executa o caso de uso
            patient = self.call_use_case.execute() # Retorna Optional[Patient]
            
            # 2. Abre a janela de resultado (mesmo se 'patient' for None)
            if self.call_window is None or not self.call_window.winfo_exists():
                self.call_window = CallResultWindow(
                    master=self,
                    patient=patient # Passa o resultado (Paciente ou None)
                )
                self.call_window.grab_set()
            else:
                self.call_window.focus()
                
        except SystemError as e:
            # TODO: Mostrar erro em um popup
            print(f"Erro no caso de uso 'Chamar': {e}")
            # (Poderíamos criar um CallResultWindow(master=self, error=e)
            # mas por enquanto só logamos no console)

    def show_status_window(self):
        """Ação para o botão 'Status'."""
        print("[GUI] Clicou em 'Status'.")

        if self.status_window is None or not self.status_window.winfo_exists():
            self.status_window = StatusWindow(
                master=self,
                status_uc=self.status_use_case
            )
            self.status_window.grab_set()
        else:
            self.status_window.focus()
            
    def quit_app(self):
        """Fecha a aplicação."""
        print("[GUI] Clicou em 'Sair'. Encerrando...")
        self.destroy()


# --- Ponto de Entrada Principal da Aplicação ---
if __name__ == "__main__":
    print("[App GUI] Inicializando a aplicação...")
    
    # 1. Configura o back-end (Composition Root)
    try:
        print("[Setup] Montando árvore de triagem...")
        triage_tree = montar_arvore()
        
        print("[Setup] Criando repositório de filas em memória...")
        queue_repo = InMemoryQueueRepository()
        
        print("[Setup] Injetando dependências nos casos de uso...")
        
        # --- LÓGICA ATUALIZADA ---
        # RegisterPatientUseCase agora só precisa do repo
        register_uc = RegisterPatientUseCase(queue_repo) 
        call_uc = CallNextPatientUseCase(queue_repo)
        status_uc = GetQueuesStatusUseCases(queue_repo)
        
        print("[App GUI] Back-end configurado com sucesso.")

        # 2. Cria a instância da App (GUI) e injeta as dependências
        app = App(
            register_uc=register_uc,
            call_uc=call_uc,
            status_uc=status_uc,
            triage_tree=triage_tree # <-- Passa a árvore para a App
        )
        
        # 3. Inicia o loop principal da interface gráfica
        print("[App GUI] Iniciando loop principal (mainloop)...")
        app.mainloop()
        
    except SystemError as e:
        print(f"\n[ERRO CRÍTICO NA INICIALIZAÇÃO]: {e}")
        # Idealmente, mostrar um popup de erro
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO DESCONHECIDO NA INICIALIZAÇÃO]: {e}")
        sys.exit(1)
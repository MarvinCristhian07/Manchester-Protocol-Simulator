import customtkinter
from typing import Optional
from src.domain.patient import Patient
from src.domain.classification import Classification
from src.domain.triage_node import NodoArvore
from src.application.use_cases.register_patient import RegisterPatientUseCase
from src.application.services.triage_service import TriageNavigator

class TriageWindow(customtkinter.CTkToplevel):
    """
    Janela "popup" para o processo de cadastro e triagem.
    """
    def __init__(self, 
                 master: customtkinter.CTk, 
                 register_uc: RegisterPatientUseCase, 
                 triage_tree: NodoArvore):
        
        super().__init__(master)
        
        # Configurações da janela
        self.title("1. Cadastrar e Iniciar Triagem")
        self.geometry("450x300")
        self.minsize(400, 250)
        
        # Dependências
        self.register_use_case = register_uc
        self.triage_tree = triage_tree
        self.navigator: Optional[TriageNavigator] = None
        self.patient: Optional[Patient] = None
        
        # --- CORREÇÃO DA FONTE (EMOJI) ---
        # Define a fonte que sabe renderizar emojis e a armazena
        # Usamos size 18 e bold para bater com o estilo do result_label
        self.emoji_font = customtkinter.CTkFont(family="Segoe UI Emoji", size=18, weight="bold")
        # --- FIM DA CORREÇÃO ---

        # --- Widgets ---
        
        # Frame de Cadastro (Nome)
        self.name_frame = customtkinter.CTkFrame(self)
        self.name_frame.pack(padx=20, pady=20, fill="x")
        
        self.name_label = customtkinter.CTkLabel(self.name_frame, text="Nome do Paciente:")
        self.name_label.pack(pady=(5, 5))
        
        self.name_entry = customtkinter.CTkEntry(self.name_frame, width=250)
        self.name_entry.pack(pady=(0, 10))
        
        self.start_button = customtkinter.CTkButton(self.name_frame, text="Iniciar Triagem", command=self.start_triage)
        self.start_button.pack(pady=(0, 10))

        # Frame de Triagem (Perguntas)
        self.triage_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        # .pack() será chamado em 'start_triage'
        
        self.question_label = customtkinter.CTkLabel(self.triage_frame, text="Pergunta...", font=customtkinter.CTkFont(size=16), wraplength=380)
        self.question_label.pack(pady=(10, 20))

        self.button_frame = customtkinter.CTkFrame(self.triage_frame, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.yes_button = customtkinter.CTkButton(self.button_frame, text="SIM", width=100, command=lambda: self.answer(True))
        self.yes_button.pack(side="left", padx=10)
        
        self.no_button = customtkinter.CTkButton(self.button_frame, text="NÃO", width=100, command=lambda: self.answer(False))
        self.no_button.pack(side="right", padx=10)

        # Frame de Resultado
        self.result_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        # .pack() será chamado em 'show_result'
        
        # O label é configurado com o texto inicial.
        # A fonte e a cor serão definidas no show_result()
        self.result_label = customtkinter.CTkLabel(self.result_frame, text="Resultado:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.result_label.pack(pady=(10, 10))
        
        self.close_button = customtkinter.CTkButton(self.result_frame, text="Fechar", command=self.destroy)
        self.close_button.pack(pady=10)


    def start_triage(self):
        """Inicia o processo de triagem após pegar o nome."""
        patient_name = self.name_entry.get().strip()
        
        try:
            # 1. Valida e cria o Paciente
            self.patient = Patient(name=patient_name)
        except ValueError as e:
            # Mostra o erro na própria tela de cadastro
            self.name_label.configure(text=f"Erro: {e}", text_color="red")
            return

        # 2. Inicializa o Navegador
        self.navigator = TriageNavigator(self.triage_tree)
        
        # 3. Esconde o frame de nome e mostra o frame de perguntas
        self.name_frame.pack_forget()
        self.triage_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # 4. Faz a primeira pergunta
        self.ask_next_question()

    def ask_next_question(self):
        """Atualiza a UI com a próxima pergunta."""
        if self.navigator.is_finished():
            # Acabou
            self.show_result()
        else:
            # Próxima pergunta
            question = self.navigator.get_current_question()
            self.question_label.configure(text=question)

    def answer(self, answer_is_yes: bool):
        """Processa a resposta (Sim/Não) do usuário."""
        self.navigator.navigate(answer_is_yes)
        self.ask_next_question() # Pergunta de novo (ou mostra resultado)

    def show_result(self):
        """Mostra o resultado final da triagem."""
        classification = self.navigator.get_final_classification()
        
        # Salva no repositório
        try:
            self.register_use_case.execute(self.patient, classification)
            
            # Atualiza a UI com o resultado
            self.triage_frame.pack_forget()
            self.result_frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            # --- CORREÇÃO DO LABEL DE RESULTADO ---
            # 1. Usa a 'self.emoji_font' (definida no __init__)
            # 2. Usa 'text_color' para colorir o texto com o hex_color
            self.result_label.configure(
                text=f"Paciente: {self.patient.name}\n\n"
                     f"{classification.color} {classification.description}",
                font=self.emoji_font, # <-- FONTE CORRIGIDA
                text_color=classification.hex_color # <-- COR DO TEXTO CORRIGIDA
            )
            # --- FIM DA CORREÇÃO ---
            
        except (ValueError, SystemError) as e:
            # Erro ao salvar
            self.result_label.configure(text=f"Erro ao salvar: {e}", text_color="red")

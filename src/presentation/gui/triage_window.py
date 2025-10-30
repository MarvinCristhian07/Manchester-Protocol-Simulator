import customtkinter
from typing import Optional
from src.domain.patient import Patient
from src.domain.classification import Classification
from src.domain.triage_node import NodoArvore
from src.application.use_cases.register_patient import RegisterPatientUseCase
from src.application.services.triage_service import TriageNavigator

class TriageWindow(customtkinter.CTkToplevel):
    '''
    Janela "popup" para o processo de cadastro e triagem
    '''
    def __init__(self, 
                 master: customtkinter.CTk, 
                 register_uc: RegisterPatientUseCase, 
                 triage_tree: NodoArvore):
        
        super().__init__(master)
        
        # Configurações da janela
        self.title("1. Cadastrar e Iniciar Triagem")
        self.geometry("450x300")
        self.minsize(400, 250)
        
        self.register_use_case = register_uc
        self.triage_tree = triage_tree
        self.navigator: Optional[TriageNavigator] = None
        self.patient: Optional[Patient] = None
        
        self.emoji_font = customtkinter.CTkFont(family="Segoe UI Emoji", size=18, weight="bold")
        
        # Frame de Cadastro
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

        self.result_label = customtkinter.CTkLabel(self.result_frame, text="Resultado:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.result_label.pack(pady=(10, 10))
        
        self.close_button = customtkinter.CTkButton(self.result_frame, text="Fechar", command=self.destroy)
        self.close_button.pack(pady=10)


    def start_triage(self):
        # Iniciar o processo de triagem após pegar o nome
        patient_name = self.name_entry.get().strip()
        
        try:
            # Validar e criar o Paciente
            self.patient = Patient(name=patient_name)
        except ValueError as e:
            # Mostrar o erro na própria tela de cadastro
            self.name_label.configure(text=f"Erro: {e}", text_color="red")
            return

        # Inicializar o Navegador
        self.navigator = TriageNavigator(self.triage_tree)
        
        # Esconder o frame de nome e mostrar o frame de perguntas
        self.name_frame.pack_forget()
        self.triage_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Fazer a primeira pergunta
        self.ask_next_question()

    def ask_next_question(self):
        # Atualizar a interface com a próxima pergunta
        if self.navigator.is_finished():
            self.show_result()
        else:
            # Próxima pergunta
            question = self.navigator.get_current_question()
            self.question_label.configure(text=question)

    def answer(self, answer_is_yes: bool):
        # Processar a resposta (Sim/Não) do usuário
        self.navigator.navigate(answer_is_yes)
        self.ask_next_question()

    def show_result(self):
        # Mostrar o resultado final da triagem
        classification = self.navigator.get_final_classification()
        
        # Salvar no repositório
        try:
            self.register_use_case.execute(self.patient, classification)
            
            # Atualiza a UI com o resultado
            self.triage_frame.pack_forget()
            self.result_frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            self.result_label.configure(
                text=f"Paciente: {self.patient.name}\n\n"
                     f"{classification.color} {classification.description}",
                font=self.emoji_font,
                text_color=classification.hex_color
            )
            
        except (ValueError, SystemError) as e:
            self.result_label.configure(text=f"Erro ao salvar: {e}", text_color="red")

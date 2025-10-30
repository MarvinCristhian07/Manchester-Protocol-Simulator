import customtkinter
from typing import Optional
from src.domain.patient import Patient

class CallResultWindow(customtkinter.CTkToplevel):
    '''
    Janela "popup" para exibir o resultado da chamada do
    próximo paciente (Botão 2)
    '''
    def __init__(self, 
                 master: customtkinter.CTk, 
                 patient: Optional[Patient]):
        
        super().__init__(master)
        
        # Configurações da janela
        self.title("2. Próximo Paciente")
        self.geometry("400x200")
        self.minsize(350, 180)
        
        # Frame principal
        main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        # A lógica da UI depende do resultado
        if patient:
            # Paciente encontrado
            title_label = customtkinter.CTkLabel(
                main_frame, 
                text="Próximo Paciente:",
                font=customtkinter.CTkFont(size=16)
            )
            title_label.grid(row=0, column=0, padx=10, pady=(10, 5))

            # Exibir o nome do paciente em destaque
            patient_name_label = customtkinter.CTkLabel(
                main_frame,
                text=patient.name.upper(),
                font=customtkinter.CTkFont(size=24, weight="bold"),
                text_color="#3182CE"
            )
            patient_name_label.grid(row=1, column=0, padx=10, pady=(5, 20))

        else:
            # Filas vazias
            title_label = customtkinter.CTkLabel(
                main_frame, 
                text="Todas as filas estão vazias.",
                font=customtkinter.CTkFont(size=18, weight="bold")
            )
            title_label.grid(row=0, column=0, padx=10, pady=(10, 20))
            
            info_label = customtkinter.CTkLabel(
                main_frame,
                text="Nenhum paciente para chamar.",
                font=customtkinter.CTkFont(size=14)
            )
            info_label.grid(row=1, column=0, padx=10, pady=(0, 20))
        
        # Botão de Fechar
        close_button = customtkinter.CTkButton(self, text="OK", command=self.destroy, width=100)
        close_button.pack(pady=(0, 20), side="bottom")

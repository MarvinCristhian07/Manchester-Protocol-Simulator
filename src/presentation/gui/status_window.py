import customtkinter
from typing import Optional, Dict
from src.domain.classification import Classification
from src.application.use_cases.get_queues_status import GetQueuesStatusUseCases

class StatusWindow(customtkinter.CTkToplevel):
    '''
    Janela "popup" para exibir o status (tamanho) de todas as filas
    '''
    def __init__(self, 
                 master: customtkinter.CTk, 
                 status_uc: GetQueuesStatusUseCases):
        
        super().__init__(master)
        
        # Configurações da janela
        self.title("3. Status das Filas")
        self.geometry("350x400")
        self.minsize(300, 350)
        self.status_use_case = status_uc
        
        # Frame principal
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        title_label = customtkinter.CTkLabel(
            main_frame, 
            text="Pacientes na Fila", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))
        
        # Cabeçalho da Tabela
        header_frame = customtkinter.CTkFrame(main_frame, fg_color="gray20")
        header_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=2)
        header_frame.grid_columnconfigure(1, weight=1)

        header_label_1 = customtkinter.CTkLabel(
            header_frame, 
            text="Classificação", 
            font=customtkinter.CTkFont(weight="bold"),
            text_color="white"
        )
        header_label_1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        header_label_2 = customtkinter.CTkLabel(
            header_frame, 
            text="Qtd.", 
            font=customtkinter.CTkFont(weight="bold"),
            text_color="white"
        )
        header_label_2.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        # Carregar e exibir os dados
        
        try:
            # Chamar o Caso de Uso para buscar os dados
            status_dict = self.status_use_case.execute()
            
            # Ordenar os dados por prioridade
            sorted_status = sorted(status_dict.items(), key=lambda item: item[0].priority)
            
            total = 0
            current_row = 2
            
            emoji_font = customtkinter.CTkFont(family="Segoe UI Emoji", size=14)

            for classification, size in sorted_status:
                total += size

                class_label = customtkinter.CTkLabel(
                    main_frame, 
                    text=f"{classification.color} {classification.name}",
                    font=emoji_font,
                    text_color=classification.hex_color
                )
                class_label.grid(row=current_row, column=0, padx=20, pady=8, sticky="w")
                
                # Label da Contagem
                size_label = customtkinter.CTkLabel(
                    main_frame, 
                    text=str(size),
                    font=customtkinter.CTkFont(size=14, weight="bold")
                )
                size_label.grid(row=current_row, column=1, padx=20, pady=8, sticky="e")
                
                current_row += 1
            
            # Linha do total
            total_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
            total_frame.grid(row=current_row, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")
            total_frame.grid_columnconfigure(0, weight=1)

            total_label_text = customtkinter.CTkLabel(total_frame, text="TOTAL DE PACIENTES:", font=customtkinter.CTkFont(weight="bold"))
            total_label_text.grid(row=0, column=0, sticky="w", padx=10)
            
            total_label_num = customtkinter.CTkLabel(total_frame, text=str(total), font=customtkinter.CTkFont(size=16, weight="bold"))
            total_label_num.grid(row=0, column=1, sticky="e", padx=10)
            
        except SystemError as e:
            # Mostrar erro se o back-end falhar
            error_label = customtkinter.CTkLabel(
                main_frame, 
                text=f"Erro ao carregar dados:\n{e}", 
                text_color="red",
                wraplength=250
            )
            error_label.grid(row=2, column=0, columnspan=2, padx=10, pady=20)
        
        # Botão de Fechar
        close_button = customtkinter.CTkButton(self, text="Fechar", command=self.destroy, width=100)
        close_button.pack(pady=(0, 20), side="bottom")

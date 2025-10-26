import uuid
from dataclasses import dataclass, field
from typing import Self

@dataclass
class Patient:
    '''
    Representa um paciente no sistema de triagem.

    Utiliza o @dataclass para gerar automaticamente métodos como:
    __init__(), __repr__(), e __eq__()
    '''

    # Aqui temos um atributo público, pois dataclasses são usadas para guardar dados
    name: str

    # field -> permite customizar atributos
    # default_factory -> chama uma função (uuid.uuid4) para criar um valor padrão
    # init=False -> significa que este campo não deve ser incluído no construtor
    # repr=False -> esconde este campo longo da impressão padrão
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False, repr=False)

    def __post_init__(self):
        # Método de validação chamado automaticamente pelo dataclass após a inicialização
        try:
            if not self.name or not isinstance(self.name, str) or self.name.strip() == "":
                # Erro para nome inválido
                raise ValueError("O nome do paciente deve ser uma string não vazia.")
            
            # Sanitiza o input removendo espaços extras
            self.name = self.name.strip()

        except AttributeError as e:
            # Captura o erro se self.name for None
            raise ValueError("O nome do paciente não pode ser 'None'.") from e
        
    def __str__(self) -> str:
        # Retorna uma representação legível do paciente
        return f"Paciente(Nome: '{self.name}')"
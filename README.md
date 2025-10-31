# Manchester Protocol Simulator
Repositório destinado ao projeto avaliativo da matéria de Estruturas de Dados do 2° Semestre do curso de Inteligência Artificial da Fatec de Rio Claro - SP.

## Proposta de Atividade 📋
Implementar, em Python, um sistema de triagem de pacientes baseado no Protocolo de Manchester.
O sistema deve:
<details>
<summary><strong>Utilizar uma árvore de decisão</strong> para classificar o nível de urgência do paciente.</summary>
  
* Cada <strong>nó</strong> da árvore representa uma <strong>pergunta de triagem</strong> (exemplo: "O paciente está respirando?").
* As <strong>folhas</strong> da árvore indicam a <strong>classificação final</strong>, com uma <strong>cor</strong>:
  
  | Cor                    | Classificação                          | 
  |------------------------|----------------------------------------|
  | 🟥 Vermelho            | Emergência (atendimento imediato)      | 
  | 🟧 Laranja             | Muito urgente                          | 
  | 🟨 Amarelo             | Urgente                                |
  | 🟩 Verde               | Pouco urgente                          |
  | 🟦 Azul                | Não urgente                            | 
</details>

<details>
<summary><strong>Inserir pacientes em filas separadas por cor,</strong> conforme o resultado da triagem.</summary> <br>

* Cada fila deve funcionar como uma <strong>estrutura de dados FIFO¹</strong>.
1. FIFO: Uma estrutura FIFO (First-In, First-Out) é um método de organização e processamento de dados onde o primeiro item a entrar na estrutura (uma lista, por exemplo) é também o primeiro a sair. Na programação, isso é comumente implementado usando uma estrutura de dados chamada Fila (Queue). Novos elementos são adicionados ao final ("fim da fila") e os elementos são removidos do início ("início da fila").
</details>

<details>
<summary>Permitir <strong>operações</strong> para gerenciar registros.</summary>
<br>
1 - Cadastrar paciente → o programa faz as perguntas da árvore e insere na fila correspondente. <br>
2 - Chamar paciente → remove e mostra o próximo paciente da fila mais urgente disponível (Vermelho > Laranja > Amarelo > Verde > Azul). <br>
3 - Mostrar status → exibe o tamanho de cada fila. <br>
0 - Sair.
</details>

O sistema deve rodar em loop até o usuário decidir encerrar.

## Estrutura esperada 🛠️
<strong>Classe NodoArvore:</strong> representa um nó da árvore de decisão. <br>
<strong>Classe Fila:</strong> implementação de fila (com enqueue e dequeue).

## Funções principais ✅
montar_arvore() → cria a árvore do protocolo (pode ser simplificada). <br>
triagem(arvore) → percorre a árvore com perguntas até chegar em uma cor. <br>
main() → loop principal com o menu.

## Sugestão de lógica da árvore (versão simplificada) 🌳
```
Está respirando?
├──── Não → Vermelho
└──── Sim → Está consciente?
   ├──── Não → Laranja
   └──── Sim → Está com dor intensa?
      ├──── Sim → Amarelo
      └──── Não → Verde
```

## Rúbrica de Avaliação (100 pontos) 🔟

| Critério                            | Descrição                                                                                                                           | Pontos |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|--------|
| Estrutura de dados da árvore        | Implementou corretamente a árvore de decisão (nós, folhas, percorrimento)                                                           |   20   |
| Estrutura de filas                  | Implementou filas separadas para cada nível de prioridade                                                                           |   20   |
| Correta classificação de pacientes  | Triagem segue corretamente a lógica da árvore                                                                                       |   20   |
| Chamada de pacientes por prioridade | Sistema chama corretamente o próximo paciente conforme urgência                                                                     |   20   |
| Interação com o usuário             | Interface de menu funcional e compreensível                                                                                         |   20   |
| Compartilhamento no Github          | Link do repositório do projeto e README.md que facilite o entendimento por pessoas que não estejam na disciplina Estrutura de Dados |   20   |

---

# Storyboard do projeto 🕖

## 26/10/2025 - Domingo
Hoje terminei de estruturar as pastas, diretórios e arquivos do meu projeto. E seguindo as boas práticas e as diretrizes do Clean-Architecture, decidi começar a programar pelo back-end e começar pela camada mais interna, o Domínio (Domain):

<strong>1. Classificação:</strong> ```src/domain/classification.py``` → Criar um arquivo para definir as classificações. Usar uma Enum (Enumeração) do Python para boas prática. Torna o código mais legível, seguro (evita erros de digitação como "Vermlho") e centraliza as regras. <br><br>
<strong>2. Estrutura da Fila:</strong> ```src/domain/custom_queue.py``` → Usar collections.deque, uma lista duplamente encadeada otimizada para operações de append (enfileirar) e popleft (desenfileirar), ambas com custo O(1). <br><br>
<strong>3. Entidade Paciente:</strong> ```src/domain/patient.py``` → Criar uma classe para representar o paciente. Em vez de uma classe padrão, usei um @dataclass, que é uma forma moderna e limpa (introduzida no Python 3.7) de criar classes que servem principalmente para armazenar dados. <br><br>
<strong>4. Entidade Nó da Árvore:</strong> ```src.domain.triage_node.py``` → Criar o arquivo NodoArvore. Esta classe é o "tijolo" da nossa árvore de decisão. Um nó, pode ser de dois tipos: Um Nó de Pergunta (interno), que tem uma pergunta e dois filhos (yes_child e no_child). Ou um Nó de Classificação (folha), que tem a cor/classificação final e não tem filhos.

Com isso, finalizo a camada Domain, podendo subir uma nível na arquitetura do projeto, a Infraestrutura (infrastructure).

## 27/10/2025 - Segunda-feira
Seguindo a Clean Architecture, defini um "contrato" na camada Application, e criei a implementação na camada de Infrastructure:

<strong>1. Interface do repositório de filas:</strong> ```src/application/interfaces/i_queue_repository.py``` → Aqui eu defino um Contrato (uma "Interface Abstrata") na camada application. Esse contrato diz o que um repositório de filas deve fazer, sem necessariamente se importar como ele faz. Ex: adicionar um paciente, chamar o próximo paciente. <br><br>
<strong>2. Implementação do Repositório em Memória:</strong> ```src/infrastructure/repositories/in_memory_repository.py``` → Criei o InMemoryQueueRepository. Ele vai herdar da interface (IQueueRepository) e implementar os três métodos definidos, usando as classes Fila e Classification criadas no domínio.

Agora tenho todo o alicerce. Tenho as Entidades (domain), o Construtor da Árvore (infrastructure), o Navegador da Triagem (application/services) e o Gerenciador das Filas (infrastructure/repositories). Com isso, posso partir para a construção dos casos de uso.

## 28/10/2025 - Terça-feira
Back-end concluído! Finalizei toda a lógica de negócio, casos de uso e implementação do sistema:

<strong>1. Serviço de triagem:</strong> ```src/application/services/triage_service.py``` → Aqui eu crio o arquivo que orquestra toda a lógica de negócio. A função triagem está criada, e esse serviço vai navegar a árvore, percorrendo por cada uma das perguntas e validar as entradas do usuário. <br><br>
<strong>2. Caso de Uso Registrar Paciente:</strong> ```src/application/use_cases/register_patient.py``` → O algoritmo responsável por registrar um paciente, recebendo o nome do paciente, criando o objeto paciente e chamando as funções e serviços das perguntas e classificação. <br><br>
<strong>3. Caso de Uso Chamar Próximo Paciente:</strong> ```src/application/use_cases/call_next_patient.py``` → Este arquivo define a lógica para chamar o próximo paciente, respeitando a ordem de prioridade (Vermelho > Laranja > Amarelo > Verde > Azul). <br><br>
<strong>4. Caso de Uso Obter Status das Filas</strong> ```src/application/use_cases/get_queues_status.py``` → Este arquivo define a lógica para consultar o tamanho das filas e o total de pacientes registrados.

Agora tenho todo o back-end feito, falta apenas criar o ponto de entrada com o loop do menu main().

## 29/10/2025 - Quarta-feira
Criando Ponto de entrada com o menu em loop principal do sistema:

<strong>1. Ponto de Entrada / UI de Console:</strong> ```src/presentation/console/main.py``` → Nesse arquivo eu crio a função main(), com o loop do menu e as funções auxiliares para tratar as entradas e saídas do usuário.

Agora tenho todo o back-end feito, e o loop do menu main() criado, posso partir pra criar as interfaces (GUI).

## 29/10/2025 - Quinta-feira
Criando as interfaces do sistema (GUI). Para isso, utilizei a biblioteca CustomTKinter:

<strong>1. UI Gráfica (CustomTkinter):</strong> ```src/presentation/gui/app.py``` → Este arquivo tem a mesma função do meu main.py, mas agora, para lidar com as interfaces do sistema. <br><br>
<strong>2. A Janela de Triagem (GUI):</strong> ```src/presentation/gui/triage_window.py``` → Este arquivo é a janela popup (Toplevel) que faz a triagem passo a passo. <br><br>
<strong>3. A Janela de Status:</strong> ```src/presentation/gui/status_window.py``` → Este arquivo chama o GetQueuesStatusUseCase assim que for aberta (__init__) e usa os dados para construir a interface e mostrar as filas. <br><br>
<strong>4. Janela de Resultado da Chamada:</strong> ```src/presentation/gui/call_result_window.py``` → E este arquivo é o popup que mostra quem foi chamado ou se as filas estão vazias.

Com isso, finalizo o projeto, com back-end e front-end prontos e funcionais. A interface está bem simples devido ao tempo para a entrega do projeto. Mas foi uma ótima experiência e prática.

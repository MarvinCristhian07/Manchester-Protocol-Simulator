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
| Correta classificação de pacientes  | Triagem segue corretamente a lógica da árvore                                                                                       |   15   |
| Chamada de pacientes por prioridade | Sistema chama corretamente o próximo paciente conforme urgência                                                                     |   15   |
| Interação com o usuário             | Interface de menu funcional e compreensível                                                                                         |   10   |
| Compartilhamento no Github          | Link do repositório do projeto e README.md que facilite o entendimento por pessoas que não estejam na disciplina Estrutura de Dados |   20   |

---

## Diário de Bordo do Projeto (Storyboard) 🕖

Todo o histórico de desenvolvimento, organização de pastas e decisões de arquitetura (Clean Architecture) que tomei durante a criação deste projeto foi documentado em um diário de bordo.

➡️ **[Clique aqui para ler o Diário de Bordo (Storyboard) completo](./STORYBOARD.md)**

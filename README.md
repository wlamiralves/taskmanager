<h1 align="center">📂Task Manager</h1>

<p align="center">
  <img alt="projeto taskmanager" src="https://github.com/user-attachments/assets/7ec02dd1-845a-4698-b5b1-f82658693ad3" width="100%">
</p>

## 🛠️ Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- Python: Linguagem de programação principal.
- Tkinter: Biblioteca para criação da interface gráfica.
- SQLite: Banco de dados utilizado para armazenar informações sobre tarefas removidas e relatórios gerados.
- CSV: Formato de arquivo para exportação e importação de tarefas

## 💻 Projeto

O Task Manager é uma aplicação de desktop intuitiva desenvolvida em Python, utilizando a biblioteca Tkinter para a interface gráfica e SQLite para gerenciamento de dados, esta aplicação oferece uma interface gráfica intuitiva para o gerenciamento de tarefas, permitindo aos usuários adicionar, editar, emitir relatórios, remover e restaurar tarefas. Este aplicativo é projetado para ajudar os usuários a gerenciar suas tarefas de forma eficiente e organizada.

## 🚀 Funcionalidades
- Adicionar Tarefas: Insira novas tarefas com definição de prioridade (alta, média, baixa) e veja-as listadas com cores diferentes para cada nível de prioridade.
- Editar Tarefas: Modifique tarefas existentes e atualize suas prioridades.
- Remover Tarefas: Exclua tarefas e mova-as para uma "Lixeira" onde podem ser restauradas ou excluídas permanentemente.
- Restaurar Tarefas: Recupere tarefas removidas da lixeira e reinclua-as na lista de tarefas.
- Emitir Relatórios: Gere relatórios CSV das tarefas para uma data específica, facilitando a análise e o acompanhamento das atividades.
- Interface Intuitiva: Design com uma interface gráfica clara e fácil de usar, com opções de estilo e cor para melhor visualização das tarefas.
- Persistência de Dados: As tarefas são salvas e carregadas de um arquivo CSV, e o histórico de tarefas excluídas é armazenado em um banco de dados SQLite para garantir que 
  nenhuma informação seja perdida.

## 💡 Como Funciona

- Adicionar Tarefas: Insira novas tarefas e defina a prioridade através da interface gráfica, alta = vermelho, média= laranja, baixa = verde.
- Editar e Remover: Selecione a tarefea, Modifique tarefas existentes ou remova-as, com a possibilidade de restaurar tarefas removidas da lixeira.
- Emitir Relatórios: Gere relatórios detalhados das tarefas com base em uma data especificada ex: dd/mm/yyyy = 25042024 será a data de início e escolha uma data final. 
- Persistência e Recuperação: As tarefas são salvas em um arquivo CSV e as tarefas excluídas são armazenadas em um banco de dados SQLite para possível restauração futura.
- Visualização de tarefas: Doubleclick na tarefa localizada na lista, ela será exibida completamente em uma janela com detalhes de data, hora e prioridade classificada.



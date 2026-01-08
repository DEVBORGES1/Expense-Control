# Documentação Técnica - Expense Control

Este documento fornece uma visão geral técnica da estrutura e funcionamento do projeto Expense Control.

## Arquitetura do Projeto

O projeto segue uma estrutura modular, separando a lógica de interface do usuário, manipulação de dados e utilitários.

### Estrutura de Diretórios

*   **Raiz:** Contém os pontos de entrada (`main.py`, `iniciar.bat`), configuração de dependências (`requirements.txt`) e scripts de dados (`seed_data.py`).
*   **ui/:** Contém os componentes da Interface Gráfica do Usuário (GUI) construídos com a biblioteca `customtkinter`.
    *   `app.py`: Classe principal que gerencia a janela da aplicação e a navegação entre telas.
    *   `login.py`: Tela de autenticação e registro de usuários.
    *   `dashboard.py`: Tela principal contendo visualizações de dados, gráficos e formulários de entrada.
*   **data/:** Responsável pela persistência de dados.
    *   `DATA.db`: Arquivo do banco de dados SQLite.
    *   `database.py` (implícito): Gerencia a conexão e consultas ao banco de dados SQLite.
*   **utils/:** Funções auxiliares e lógicas de negócio específicas.
    *   `gamification.py`: Lógica para cálculo de níveis e progresso do usuário.

## Banco de Dados

O sistema utiliza SQLite para armazenamento local. As principais entidades gerenciadas incluem:

*   **Usuários:** Credenciais e informações de perfil.
*   **Transações:** Registros financeiros de entrada (receitas) e saída (despesas).
*   **Categorias:** Classificação das transações.
*   **Orçamentos:** Limites definidos pelo usuário para categorias específicas.
*   **Lista de Desejos:** Metas financeiras do usuário.

## Bibliotecas Principais

*   **customtkinter:** Framework de UI para criação de interfaces modernas e responsivas no desktop.
*   **matplotlib:** Utilizado para geração dos gráficos de pizza e linha no dashboard.
*   **pandas:** Manipulação e análise de dados para geração de relatórios e gráficos.
*   **pillow (PIL):** Manipulação de imagens e ícones.
*   **bcrypt:** Hashing seguro para armazenamento de senhas.

## Fluxo de Autenticação

1.  O usuário insere credenciais na tela de Login.
2.  O sistema verifica o hash da senha no banco de dados.
3.  Em caso de sucesso, o ID do usuário é recuperado e passado para o `DashboardFrame`, carregando os dados específicos daquele usuário.

## Sistema de Gamificação

O sistema de gamificação incentiva a poupança. A lógica reside principalmente em calcular o saldo acumulado (Receitas - Despesas) e converter esse valor em "experiência" ou níveis. O progresso é exibido visualmente no Dashboard.

## Desenvolvimento e Manutenção

Para modificar ou estender o projeto:

1.  **Interface:** Alterações visuais devem ser feitas nos arquivos dentro da pasta `ui/`. O `customtkinter` permite ajustes de tema (Claro/Escuro) e cores.
2.  **Dados:** Novas consultas ou modificações no esquema devem ser tratadas na camada de dados.
3.  **Dependências:** Ao adicionar novas bibliotecas, lembre-se de atualizar o arquivo `requirements.txt`:
    ```bash
    pip freeze > requirements.txt
    ```

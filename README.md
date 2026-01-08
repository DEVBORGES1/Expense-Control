# Expense Control

O Expense Control é uma aplicação desktop desenvolvida em Python para gerenciamento de finanças pessoais. O sistema oferece uma interface moderna para rastreamento de receitas e despesas, definição de orçamentos e acompanhamento de metas financeiras. Além disso, incorpora elementos de gamificação para incentivar hábitos de economia saudáveis.

## Funcionalidades Principais

*   **Painel de Controle (Dashboard):** Visão geral da saúde financeira com gráficos de crescimento e distribuição de gastos.
*   **Gestão de Transações:** Registro detalhado de receitas e despesas com categorização e datas.
*   **Orçamentos:** Definição de limites de gastos por categoria (ex: Comida, Lazer, Transporte) para melhor controle.
*   **Lista de Desejos (Wishlist):** Planejamento de compras futuras com estimativa de tempo para aquisição baseada na poupança atual.
*   **Sistema de Gamificação:** O usuário evolui de nível conforme acumula economias, tornando o processo de poupar mais engajador.

## Pré-requisitos

Para executar este projeto, você precisará ter instalado em sua máquina:

*   Python 3.8 ou superior
*   Pip (gerenciador de pacotes do Python)

## Instalação

1.  Baixe ou clone o repositório do projeto para o seu computador.
2.  Navegue até o diretório raiz do projeto através do terminal.
3.  Instale as dependências necessárias listadas no arquivo `requirements.txt` executando o seguinte comando:

    ```bash
    pip install -r requirements.txt
    ```

## Configuração Inicial (Banco de Dados)

O projeto utiliza um banco de dados local SQLite. Para configurar o banco de dados e criar um usuário inicial com dados de exemplo, execute o script de "seeding":

```bash
python seed_data.py
```

Este script criará:
*   Um usuário padrão (Usuário: `bg`, Senha: `123`).
*   Transações de exemplo (receitas e despesas).
*   Orçamentos e itens na lista de desejos.

## Como Executar

Após a instalação e configuração inicial, você pode iniciar a aplicação de duas formas:

**Opção 1: Via Script de Inicialização (Windows)**
Execute o arquivo `iniciar.bat` com um clique duplo.

**Opção 2: Via Terminal**
Execute o arquivo principal Python através do comando:

```bash
python main.py
```

## Credenciais de Acesso

Se você utilizou o script `seed_data.py`, pode acessar o sistema com as seguintes credenciais:

*   **Usuário:** bg
*   **Senha:** 123

Você também pode registrar um novo usuário diretamente na tela de login da aplicação.

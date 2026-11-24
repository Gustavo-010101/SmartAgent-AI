# 🤖 SmartAgent AI

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

## 📌 Sobre o projeto

O SmartAgent AI é um agente inteligente de atendimento ao cliente, desenvolvido para automatizar consultas de pedidos utilizando inteligência artificial generativa e integração com banco de dados.

O sistema permite que os usuários realizem perguntas em linguagem natural e recebam respostas baseadas nas informações armazenadas no MySQL.

O projeto utiliza um modelo de linguagem executado localmente por meio do Ollama, sem depender de APIs pagas de inteligência artificial.

## 🎯 Objetivos

- Automatizar consultas de pedidos.
- Facilitar o acesso às informações.
- Reduzir tarefas repetitivas no atendimento.
- Integrar inteligência artificial com bancos de dados.
- Monitorar indicadores de atendimento.
- Demonstrar a aplicação prática de IA em processos empresariais.

## 🚀 Funcionalidades

- Chat inteligente com IA generativa.
- Consulta de pedidos em linguagem natural.
- Consulta de produtos e status de entrega.
- Consulta de previsões de entrega.
- Histórico de conversas persistente.
- Criação de novas conversas.
- Renomeação de conversas.
- Exclusão de conversas.
- Exportação de conversas em TXT.
- Monitoramento da conexão com MySQL e Ollama.
- Dashboard de métricas de atendimento.
- Gráfico de atividade diária.
- Tabela interativa de pedidos.
- Pesquisa por número, cliente ou produto.
- Filtro por status dos pedidos.
- Interface responsiva com tema escuro.
- Análise inteligente de dados utilizando IA generativa.
- Contagem total de pedidos e clientes.
- Contagem de produtos, status e datas distintas.
- Análise de pedidos cancelados, atrasados e entregues.
- Ranking de produtos por quantidade de pedidos.
- Análise de pedidos por cliente.
- Comparação de indicadores operacionais.
- Consultas de dados consolidados diretamente no MySQL.
## 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Desenvolvimento da aplicação |
| Streamlit | Interface web |
| Ollama | Execução local da inteligência artificial |
| Qwen3:4b | Modelo de linguagem |
| MySQL | Armazenamento de dados |
| Pandas | Manipulação e análise de dados |
| Altair | Visualização de dados |
| Python-dotenv | Gerenciamento de variáveis de ambiente |
| Git e GitHub | Versionamento de código |

## 📸 Demonstração do sistema

![Demonstração 1](images/image.png)

![Demonstração 2](images/Captura%20de%20tela%202026-11-24%20151526.png)

![Demonstração 3](images/Captura%20de%20tela%202026-11-24%20152217.png)

![Demonstração 4](images/Captura%20de%20tela%202026-11-24%20152303.png)

```text
Usuário
   |
   v
Interface Streamlit
   |
   v
Agente inteligente Python
   |
   +------> Ollama / Qwen3:4b
   |
   +------> Banco de dados MySQL
   |
   v
Resposta ao usuário
```

## 🗄️ Banco de dados

O projeto utiliza o banco de dados `smartagent_ai`, composto por três tabelas:

| Tabela | Descrição |
|---|---|
| pedidos | Informações dos pedidos fictícios |
| historico_conversas | Registro das mensagens |
| titulos_conversas | Gerenciamento dos títulos das conversas |

A base de demonstração foi planejada com 100 pedidos fictícios, incluindo clientes, produtos, status e previsões de entrega.

## 📊 Indicadores de atendimento

- Total de conversas.
- Total de mensagens.
- Total de perguntas.
- Total de respostas da IA.
- Atividade diária de atendimento.

## 💬 Exemplos de perguntas

- Qual é o status do pedido 1001?
- Quando está prevista a entrega do pedido 1003?
- Qual produto pertence ao pedido 1004?
- Qual é o produto e o status do pedido 1015?

## 📁 Estrutura do projeto

```text
SmartAgent-AI/
├── .streamlit/
│   └── config.toml
├── .env.example
├── .gitignore
├── agente.py
├── app.py
├── database.py
├── database.sql
├── requirements.txt
└── README.md
```

## ⚙️ Instalação e execução

### 1. Pré-requisitos

- Python 3.12
- MySQL Server
- Ollama
- Git

### 2. Clonar o repositório

```bash
git clone https://github.com/Gustavo-010101/SmartAgent-AI.git
cd SmartAgent-AI
```

### 3. Criar o ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar o banco de dados

Execute o arquivo `database.sql` no MySQL Workbench.

Crie uma cópia do arquivo `.env.example` com o nome `.env` e configure suas credenciais:

```env
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=smartagent_ai
```

### 6. Baixar o modelo de inteligência artificial

```bash
ollama pull qwen3:4b
```

Certifique-se de que o Ollama esteja em execução.

### 7. Executar a aplicação

```bash
python -m streamlit run app.py
```

Acesse o endereço informado pelo Streamlit no terminal.

## 🔒 Segurança e privacidade

- Credenciais armazenadas em variáveis de ambiente.
- Arquivo `.env` protegido pelo `.gitignore`.
- Modelo de inteligência artificial executado localmente.
- Base de demonstração composta por dados fictícios.

## 🧠 Competências demonstradas

- Inteligência artificial generativa.
- Modelos de linguagem (LLMs).
- Desenvolvimento de agentes inteligentes.
- Engenharia de prompts.
- Programação em Python.
- Banco de dados relacional.
- Integração de sistemas.
- Análise e visualização de dados.
- Automação de processos.
- Desenvolvimento de aplicações web.
- Versionamento de código.

## 👨‍💻 Desenvolvedor

**Gustavo Alves Favoreto**

Projeto desenvolvido para portfólio profissional, com foco em tecnologia, inteligência artificial, análise de dados e automação de processos empresariais.

GitHub: https://github.com/Gustavo-010101

---

⭐ Se você gostou do projeto, considere deixar uma estrela no repositório.

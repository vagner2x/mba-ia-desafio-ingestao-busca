# Desafio MBA Engenharia de Software com IA - Full Cycle

## 📋 Sobre o Projeto

Sistema de **ingestão e busca semântica** utilizando LangChain, PostgreSQL com pgVector e modelos de embeddings (OpenAI ou Google Gemini). O projeto permite:

- **Ingestão**: Leitura de arquivos PDF e armazenamento vetorizado no banco de dados
- **Busca**: Interface CLI para fazer perguntas baseadas no conteúdo do PDF

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **LangChain** - Framework para aplicações com LLM
- **PostgreSQL + pgVector** - Banco vetorial
- **OpenAI** - Embeddings e LLM
- **Docker & Docker Compose** - Containerização

## 📦 Estrutura do Projeto

```
├── docker-compose.yml         # Configuração do PostgreSQL com pgVector
├── requirements.txt           # Dependências Python
├── .env.example              # Template de variáveis de ambiente
├── src/
│   ├── ingest.py            # Script de ingestão do PDF
│   ├── search.py            # Script de busca vetorial
│   ├── chat.py              # CLI interativo
├── document.pdf             # PDF para ingestão
└── README.md                # Este arquivo
```

## ⚙️ Pré-requisitos

- **Python 3.8+** instalado
- **Docker** e **Docker Compose** instalados
- Chave de API da **OpenAI** ou **Google Gemini**

## 🔧 Configuração e Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

### 2. Crie o ambiente virtual Python

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e edite com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
# API Keys
OPENAI_API_KEY=sua-chave-openai-aqui
GOOGLE_API_KEY=sua-chave-google-aqui  # Opcional se usar OpenAI

# Modelos
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
GOOGLE_EMBEDDING_MODEL=models/embedding-001

# Banco de Dados
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag

# Configurações
PG_VECTOR_COLLECTION_NAME=gpt5_collection
PDF_PATH=./document.pdf
```

**Obtenha suas API Keys:**
- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google Gemini**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 5. Adicione seu documento PDF

Coloque o arquivo PDF que deseja ingerir na raiz do projeto com o nome `document.pdf`, ou configure o caminho correto na variável `PDF_PATH` do arquivo `.env`.

## 🎯 Como Executar

### Passo 1: Subir o banco de dados PostgreSQL

```bash
docker compose up -d
```

Verifique se os containers estão rodando:
```bash
docker compose ps
```

Você deve ver os serviços `postgres_rag` e `bootstrap_vector_ext` ativos.

### Passo 2: Executar a ingestão do PDF

```bash
python src/ingest.py
```

Este script irá:
- Carregar o PDF configurado
- Dividir em chunks de 1000 caracteres com overlap de 150
- Gerar embeddings para cada chunk
- Armazenar no banco vetorial PostgreSQL

**Saída esperada:**
```
Carregando PDF...
Dividindo em chunks...
Gerando embeddings e salvando no banco...
✓ Ingestão concluída com sucesso!
```

### Passo 3: Iniciar o chat interativo

```bash
python src/chat.py
```

Agora você pode fazer perguntas sobre o conteúdo do PDF:

```
=== Sistema de Busca Semântica ===
Digite sua pergunta (ou 'sair' para encerrar):

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

---

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

---

PERGUNTA: sair
Encerrando...
```

## 🔍 Como Funciona

### Ingestão
1. O PDF é carregado usando `PyPDFLoader`
2. Texto é dividido em chunks usando `RecursiveCharacterTextSplitter`
3. Cada chunk é convertido em embedding usando `OpenAIEmbeddings` ou `GoogleGenerativeAIEmbeddings`
4. Vetores são armazenados no PostgreSQL com `PGVector`

### Busca
1. Pergunta do usuário é vetorizada
2. Busca por similaridade retorna os 10 chunks mais relevantes (`k=10`)
3. Chunks são concatenados e enviados como contexto para o LLM
4. LLM responde baseado apenas no contexto fornecido

### Prompt Utilizado

```
CONTEXTO:
{resultados concatenados do banco de dados}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

PERGUNTA DO USUÁRIO:
{pergunta do usuário}

RESPONDA A "PERGUNTA DO USUÁRIO"
```

## 🛠️ Troubleshooting

### Erro de conexão com o banco

Se encontrar erro de conexão ao PostgreSQL:

```bash
# Verifique se o container está rodando
docker compose ps

# Veja os logs
docker compose logs postgres

# Reinicie os containers
docker compose restart
```

### Erro "ModuleNotFoundError"

Certifique-se de que o ambiente virtual está ativado:

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

E que as dependências foram instaladas:

```bash
pip install -r requirements.txt
```

### Erro de API Key

Verifique se:
- O arquivo `.env` foi criado na raiz do projeto
- A chave de API foi configurada corretamente
- Não há espaços extras na chave

## 📚 Recursos Adicionais

- [Documentação LangChain](https://python.langchain.com/)
- [pgVector GitHub](https://github.com/pgvector/pgvector)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Curso de nivelamento LangChain](https://github.com/codeedu/ia-langchain-curso-nivelamento)

## 📝 Modelos Utilizados

### OpenAI
- **Embeddings**: `text-embedding-3-small`
- **LLM**: `gpt-4` ou `gpt-3.5-turbo`

### Google Gemini
- **Embeddings**: `models/embedding-001`
- **LLM**: `gemini-2.5-flash-lite` ou `gemini-pro`

## 🧹 Limpeza

Para parar e remover os containers:

```bash
docker compose down
```

Para remover também os volumes (dados do banco):

```bash
docker compose down -v
```

## 📄 Licença

Este projeto foi desenvolvido como parte do MBA em Engenharia de Software com IA - Full Cycle.

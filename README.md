# Eleições API

## Instalação

### 1. Clone ou navegue até o projeto
```bash
cd tp2-desenvolvimento-de-api-rest-Gomez-01/eleicoes_api
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure o banco de dados PostgreSQL

Certifique-se de que PostgreSQL está em execução e crie o banco de dados:

```sql
CREATE DATABASE eleicoes_db;
```

As credenciais padrão são:
- **Usuário:** postgres
- **Senha:** postgres
- **Host:** localhost
- **Porta:** 5432

Se precisar alterar, edite `eleicoes_api/settings.py` na seção `DATABASES`.

### 6. Execute as migrações
```bash
python manage.py migrate
```

## Execução

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O servidor estará disponível em: **http://127.0.0.1:8000**

## Documentação da API

### Swagger UI
Acesse a documentação interativa Swagger em:
- **http://127.0.0.1:8000/swagger/**

### ReDoc
Acesse a documentação ReDoc em:
- **http://127.0.0.1:8000/redoc/**

### Schema OpenAPI
Obtenha o schema OpenAPI em:
- **http://127.0.0.1:8000/swagger/?format=openapi**

## Endpoints Principais

### Eleitores
- `GET /api/eleitores/` - Listar todos os eleitores
- `POST /api/eleitores/` - Criar novo eleitor
- `GET /api/eleitores/{id}/` - Obter detalhes de um eleitor
- `PUT /api/eleitores/{id}/` - Atualizar eleitor
- `DELETE /api/eleitores/{id}/` - Deletar eleitor

**Filtros:** `ativo`, `nome`, `cpf`, `email`

### Eleições
- `GET /api/eleicoes/` - Listar todas as eleições
- `POST /api/eleicoes/` - Criar nova eleição
- `GET /api/eleicoes/{id}/` - Obter detalhes de uma eleição
- `PUT /api/eleicoes/{id}/` - Atualizar eleição
- `DELETE /api/eleicoes/{id}/` - Deletar eleição

### Candidatos
- `GET /api/candidatos/` - Listar todos os candidatos
- `POST /api/candidatos/` - Criar novo candidato
- `GET /api/candidatos/{id}/` - Obter detalhes de um candidato
- `PUT /api/candidatos/{id}/` - Atualizar candidato
- `DELETE /api/candidatos/{id}/` - Deletar candidato

### Aptidão de Eleitores
- `GET /api/aptidao-eleitor/` - Listar aptidões
- `POST /api/aptidao-eleitor/` - Criar nova aptidão
- `GET /api/aptidao-eleitor/{id}/` - Obter detalhes
- `PUT /api/aptidao-eleitor/{id}/` - Atualizar aptidão
- `DELETE /api/aptidao-eleitor/{id}/` - Deletar aptidão

### Registro de Votação (somente leitura)
- `GET /api/registro-votacao/` - Listar registros de votação
- `GET /api/registro-votacao/{id}/` - Obter detalhes

### Votos (somente leitura)
- `GET /api/votos/` - Listar votos
- `GET /api/votos/{id}/` - Obter detalhes de um voto

## Validações Implementadas

- **CPF:** Formato obrigatório `000.000.000-00`
- **Email:** Deve ser único no sistema
- **Datas de Eleição:** Data de início deve ser anterior à data de fim
- **Fluxo de Status:** rascunho → aberta → encerrada → apurada (sem retrocesso)
- **Votação:** Eleitor deve estar apto, eleição deve estar aberta no período correto
- **Voto em Branco:** Não pode ter candidato associado
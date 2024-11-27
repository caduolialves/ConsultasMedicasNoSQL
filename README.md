# Sistema de Gerenciamento de Consultas Médicas
Este é um sistema simples para gerenciar médicos, pacientes e consultas médicas usando o MongoDB como banco de dados. O sistema permite inserir, listar, atualizar e remover médicos, pacientes e consultas, com funcionalidades adicionais como geração de relatórios.

## Funcionalidades

1. **Gerenciamento de Médicos**
   - Inserir médicos com nome, especialidade e telefone.
   - Listar médicos cadastrados.
   - Atualizar informações de um médico.
   - Remover um médico, garantindo que todas as consultas associadas a ele também sejam excluídas.
1. **Gerenciamento de Pacientes**
   - Inserir pacientes com nome e telefone.
   - Listar pacientes cadastrados.
   - Atualizar informações de um paciente.
   - Remover um paciente, garantindo que todas as consultas associadas a ele também sejam excluídas.
1. **Gerenciamento de Consultas**
   - Marcar consultas associando médicos e pacientes.
   - Listar consultas, exibindo informações detalhadas como médico, paciente, data, hora e status.
   - Atualizar informações de uma consulta (data, hora ou status).
   - Remover uma consulta específica.
1. **Relatórios**
   - Consultas por médico (detalhadas): Exibe todas as consultas associadas a um médico específico.
   - Total de consultas agendadas por médico: Exibe o número de consultas agendadas para cada médico.
  
## Requisitos

### Linguagem e Dependências
  - **Python 3.10+**
  - **MongoDB**
  - **Bibliotecas Python necessárias:**
      - **`pymongo`**
      - **`tabulate`**
      - **`prompt_toolkit`**
      - **`bson`**
Instale as dependências usando o comando:
```bash
pip install pymongo tabulate prompt_toolkit bson
```
## Banco de Dados
O sistema utiliza um banco de dados MongoDB com as seguintes coleções:

- `medicos`: Contém os dados dos médicos.
- `pacientes`: Contém os dados dos pacientes.
- `consultas`: Contém os dados das consultas.

## Como Usar

### 1. Inicialização
- Certifique-se de que o MongoDB está em execução.
- Configure a conexão no arquivo `config/database.py`:
```python
def get_database():
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    return client["meuBanco"]
```
### 2. Estrutura do Projeto
```plaintext
mongoDB/
├── config/
│   └── database.py          # Conexão com o MongoDB
├── controllers/
│   ├── medico_controller.py # Gerenciamento de médicos
│   ├── paciente_controller.py # Gerenciamento de pacientes
│   └── consulta_controller.py # Gerenciamento de consultas
├── utils/
│   └── selection_utils.py   # Funções auxiliares para seleção interativa
├── main.py                  # Arquivo principal para rodar o sistema
├── requirements.txt         # Dependências do projeto
└── README.md                # Este arquivo
```
### 3. Executar o Sistema
Para executar o sistema, rode o arquivo `main.py`:
```bash
python main.py
```
## Considerações
- Certifique-se de que os IDs em `medico_id` e `paciente_id` na coleção `consultas` estão armazenados como `ObjectId`.
- Use os scripts auxiliares para corrigir dados antigos, caso necessário.
- O sistema é básico e pode ser expandido com novas funcionalidades como autenticação ou interface gráfica.
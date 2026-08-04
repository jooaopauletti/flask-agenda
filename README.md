# 📋 CRUD Python com Flask - Agenda de Contatos
🔗 **Acesse a aplicação online:** https://flask-agenda-902t.onrender.com

Aplicação de agenda de contatos desenvolvida em Python com Flask e SQLite, com interface web estilizada com Bootstrap. Cada usuário possui login próprio e gerencia sua lista de contatos de forma independente.

## Funcionalidades
- 🔐 Cadastro, login e logout de usuários (senha protegida com hash)
- 👤 Contatos vinculados a cada usuário, com acesso restrito ao próprio dono
- ✅ Adicionar contatos
- 📋 Listar contatos
- ✏️ Atualizar contatos
- ❌ Deletar contatos com confirmação
- ⚠️ Validação de campos obrigatórios
- 💬 Mensagens de feedback ao usuário

## Como executar
1. Clone o repositório
2. Instale o Flask
3. Execute o arquivo `app.py`

```bash
pip install flask
python app.py
```
4. Acesse no navegador: `http://127.0.0.1:5000`

## Tecnologias
- Python 3
- Flask
- SQLite
- Bootstrap 5
- Werkzeug (hash de senha)

## Autor
João Pauletti
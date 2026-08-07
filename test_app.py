import pytest
from app import app, DB_NAME
import database
import os

@pytest.fixture
def client():
    if os.path.exists('test_agenda.db'):
        os.remove('test_agenda.db')
    database.criar_banco('test_agenda.db')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    os.remove('test_agenda.db')

def test_pagina_login_carrega(client):
    resposta = client.get('/login')
    assert resposta.status_code == 200

def test_cadastro_cria_usuario(client, monkeypatch):
    monkeypatch.setattr('app.DB_NAME', 'test_agenda.db')
    
    resposta = client.post('/cadastrar', data={
        'login': 'usuario_teste',
        'senha': 'senha123'
    }, follow_redirects=True)
    
    assert resposta.status_code == 200
    assert 'sucesso' in resposta.text

def test_login_senha_errada(client, monkeypatch):
    monkeypatch.setattr('app.DB_NAME', 'test_agenda.db')
    
    client.post('/cadastrar', data={
        'login': 'usuario_login_teste',
        'senha': 'senha_correta'
    })
    
    resposta = client.post('/entrar', data={
        'login': 'usuario_login_teste',
        'senha': 'senha_errada'
    }, follow_redirects=True)
    
    assert 'inválidos' in resposta.text

def test_cadastro_login_duplicado(client, monkeypatch):
    monkeypatch.setattr('app.DB_NAME', 'test_agenda.db')
    
    client.post('/cadastrar', data={
        'login': 'usuario_duplicado',
        'senha': 'senha123'
    })
    
    resposta = client.post('/cadastrar', data={
        'login': 'usuario_duplicado',
        'senha': 'outra_senha'
    }, follow_redirects=True)
    
    assert 'já cadastrado' in resposta.text

def test_nao_pode_deletar_contato_de_outro_usuario(client, monkeypatch):
    monkeypatch.setattr('app.DB_NAME', 'test_agenda.db')
    
    client.post('/cadastrar', data={'login': 'usuario_a', 'senha': 'senha123'})
    client.post('/entrar', data={'login': 'usuario_a', 'senha': 'senha123'})
    client.post('/adicionar', data={'nome': 'Contato A', 'telefone': '123', 'email': 'a@teste.com'})
    client.get('/logout')
    
    client.post('/cadastrar', data={'login': 'usuario_b', 'senha': 'senha123'})
    client.post('/entrar', data={'login': 'usuario_b', 'senha': 'senha123'})
    
    resposta = client.post('/deletar/1', follow_redirects=True)
    
    conn_check = __import__('sqlite3').connect('test_agenda.db')
    cursor = conn_check.cursor()
    cursor.execute('SELECT * FROM contatos WHERE id = 1')
    contato = cursor.fetchone()
    conn_check.close()
    
    assert contato is not None
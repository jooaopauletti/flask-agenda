from dotenv import load_dotenv
import os
import database
import sqlite3
from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY
database.criar_banco()

@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contatos WHERE usuario_id = ?', (session['usuario_id'],))
    contatos = cursor.fetchall()
    conn.close()
    return render_template('index.html', contatos=contatos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'usuario_id' not in session:
        return redirect('/login')
    nome = request.form['nome'].strip()
    telefone = request.form['telefone'].strip()
    email = request.form['email'].strip()
    if not nome or not telefone or not email:
        flash('Preencha todos os campos!')
        return redirect('/')  
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contatos (nome, telefone, email, usuario_id) VALUES (?, ?, ?, ?)', (nome, telefone, email, session['usuario_id']))
    conn.commit()
    conn.close()
    flash('Contato adicionado com sucesso!')
    return redirect('/')

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contatos WHERE id = ? AND usuario_id = ?', (id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contatos WHERE id = ? AND usuario_id = ?', (id, session['usuario_id']))
    contato = cursor.fetchone()
    conn.close()
    if contato is None:
        return redirect('/')
    return render_template('editar.html', contato=contato)

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    nome = request.form['nome'].strip()
    telefone = request.form['telefone'].strip()
    email = request.form['email'].strip()
    if not nome or not telefone or not email:
        flash('Preencha todos os campos!')
        return redirect('/editar/' + str(id))
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE contatos SET nome=?, telefone=?, email=? WHERE id=? AND usuario_id=?', (nome, telefone, email, id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    login = request.form['login'].strip()
    senha = request.form['senha'].strip()
    
    if not login or not senha:
        flash('Preencha todos os campos!')
        return redirect('/cadastro')
    
    senha_hash = generate_password_hash(senha)
    
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (login, senha) VALUES (?, ?)', (login, senha_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        flash('Usuário já cadastrado anteriormente!')
        return redirect('/cadastro')
    finally:
        conn.close()
    
    flash('Cadastro realizado com sucesso!')
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/entrar', methods=['POST'])
def entrar():
    login = request.form['login'].strip()
    senha = request.form['senha'].strip()
    
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario and check_password_hash(usuario[2], senha):
        session['usuario_id'] = usuario[0]
        return redirect('/')
    
    flash('Login ou senha inválidos!')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
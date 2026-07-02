from flask import Flask, render_template, request, redirect, flash
import database
import sqlite3

app = Flask(__name__)
app.secret_key = 'flask_agenda_2026'
database.criar_banco()

@app.route('/')
def index():
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contatos') 
    contatos = cursor.fetchall()
    conn.close()
    return render_template('index.html', contatos=contatos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome'].strip()
    telefone = request.form['telefone'].strip()
    email = request.form['email'].strip()
    if not nome or not telefone or not email:
        flash('Preencha todos os campos!')
        return redirect('/')  
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)', (nome, telefone, email))
    conn.commit()
    conn.close()
    flash('Contato adicionado com sucesso!')
    return redirect('/')

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contatos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/editar/<id>', methods= ['GET'])
def editar(id):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contatos WHERE id = ?', (id,))
    contato = cursor.fetchone()
    conn.close()
    return render_template('editar.html', contato=contato)

@app.route('/atualizar/<id>', methods= ['POST'])
def atualizar(id):
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE contatos SET nome=?, telefone=?, email=? WHERE id=?', (nome, telefone, email, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

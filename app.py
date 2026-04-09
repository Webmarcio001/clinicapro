
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

def get_db():
    return sqlite3.connect('database.db')

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        senha = request.form['senha']
        if user == 'admin' and senha == '123':
            session['user'] = user
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/pacientes', methods=['GET','POST'])
def pacientes():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        c.execute("INSERT INTO pacientes (nome, idade) VALUES (?,?)",(nome, idade))
        conn.commit()
    lista = c.execute("SELECT * FROM pacientes").fetchall()
    conn.close()
    return render_template('pacientes.html', pacientes=lista)

@app.route('/consultas', methods=['GET','POST'])
def consultas():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        data = request.form['data']
        c.execute("INSERT INTO consultas (nome, data) VALUES (?,?)",(nome, data))
        conn.commit()
    lista = c.execute("SELECT * FROM consultas").fetchall()
    conn.close()
    return render_template('consultas.html', consultas=lista)

if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS pacientes (id INTEGER PRIMARY KEY, nome TEXT, idade INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS consultas (id INTEGER PRIMARY KEY, nome TEXT, data TEXT)")
    conn.commit()
    conn.close()
    app.run()

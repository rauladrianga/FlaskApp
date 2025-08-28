from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def conectar():
    conn = sqlite3.connect("p.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = conectar()
    personas = conn.execute("SELECT * FROM personas").fetchall()
    conn.close()
    return render_template("index.html", personas=personas)

@app.route('/crear', methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form["nombre"]
        edad = request.form["edad"]
        conn = conectar()
        conn.execute("INSERT INTO personas (nombre, edad) VALUES (?, ?)", (nombre, edad))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("form.html", persona=None)

@app.route('/editar/<int:id>', methods=["GET", "POST"])
def editar(id):
    conn = conectar()
    persona = conn.execute("SELECT * FROM personas WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        nombre = request.form["nombre"]
        edad = request.form["edad"]
        conn.execute("UPDATE personas SET nombre = ?, edad = ? WHERE id = ?", (nombre, edad, id))
        conn.commit()
        conn.close()
        return redirect('/')
    conn.close()
    return render_template("form.html", persona=persona)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = conectar()
    conn.execute("DELETE FROM personas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Crear tabla si no existe
with conectar() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    """)
    conn.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # OJO: Cambiar host a 0.0.0.0 para que Render detecte el puerto y acceda a la app
    app.run(host='0.0.0.0', port=port, debug=True)

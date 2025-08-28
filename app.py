from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear tabla si no existe
def init_db():
    print(f"✅ Iniciando la DB")
    conn = sqlite3.connect('personas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():

    print(f"✅ Entrando a Index")
    conn = sqlite3.connect('personas.db')
    personas = conn.execute('SELECT * FROM personas').fetchall()
    conn.close()
    return render_template('index.html', personas=personas)

@app.route('/agregar', methods=['POST'])
def agregar():
    print(f"✅ Entrando a Agregar")
    try:
        nombre = request.form['nombre']
        edad = request.form['edad']
        conn = sqlite3.connect('personas.db')
        conn.execute('INSERT INTO personas (nombre, edad) VALUES (?, ?)', (nombre, edad))
        conn.commit()
        print(f"✅ Insertado: {nombre}, {edad}")
    except Exception as e:
        print("❌ Error al insertar:", e)
    finally:
        conn.close()
    return redirect('/')


@app.route('/eliminar/<int:id>')
def eliminar(id):
    print(f"✅ Entrando a Eliminar")
    conn = sqlite3.connect('personas.db')
    conn.execute('DELETE FROM personas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    print(f"✅ Entrando a Main")
    init_db()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear tabla si no existe
def init_db():
    print(f"✅ Iniciando la DB")
    conn = sqlite3.connect('citas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    print(f"✅ Entrando a Index")
    conn = sqlite3.connect('citas.db')
    citas = conn.execute('SELECT * FROM citas').fetchall()
    conn.close()
    return render_template('index.html', citas=citas)


@app.route('/agregar', methods=['POST'])
def agregar():
    print(f"✅ Entrando a Agregar")
    try:
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        fecha = request.form['fecha']
        hora = request.form['hora']

        conn = sqlite3.connect('citas.db')
        conn.execute('''
            INSERT INTO citas (nombre, edad, direccion, telefono, fecha, hora)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, edad, direccion, telefono, fecha, hora))
        conn.commit()
        print(f"✅ Insertado: {nombre}, {fecha} {hora}")
    except Exception as e:
        print("❌ Error al insertar:", e)
    finally:
        conn.close()
    return redirect('/')



@app.route('/eliminar/<int:id>')
def eliminar(id):
    print(f"✅ Entrando a Eliminar")
    conn = sqlite3.connect('citas.db')
    conn.execute('DELETE FROM citas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


init_db()
if __name__ == '__main__':
    print(f"✅ Entrando a Main")
    app.run(debug=True) 

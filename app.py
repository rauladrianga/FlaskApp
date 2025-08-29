from flask import Flask, render_template, request, redirect
from flask import Flask, send_file, render_template, request, redirect, session, url_for
from flask_mail import Mail, Message
import sqlite3
from io import BytesIO
import openpyxl

app = Flask(__name__)
app.secret_key = 'adminFlask'  # Necesario para sesiones


@app.route('/admin/descargar')
def descargar_excel():
    if not session.get('autenticado'):
        return redirect('/admin')

    conn = sqlite3.connect('citas.db')
    citas = conn.execute('SELECT * FROM citas').fetchall()
    conn.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Citas Médicas"

    # Encabezados
    columnas = ["ID", "Nombre", "Edad", "Dirección", "Teléfono", "Email", "Fecha", "Hora"]
    ws.append(columnas)

    # Datos
    for cita in citas:
        ws.append(list(cita))

    # Guardar a memoria
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output,
                     download_name="citas.xlsx",
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# Ruta de login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']

        # Verificación simple (puedes usar hash más adelante)
        if usuario == 'admin' and clave == 'admin123':
            session['autenticado'] = True
            return redirect('/admin/citas')
        else:
            return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')


# Ruta protegida con login
@app.route('/admin/citas')
def admin_citas():
    if not session.get('autenticado'):
        return redirect('/admin')

    conn = sqlite3.connect('citas.db')
    citas = conn.execute('SELECT * FROM citas').fetchall()
    conn.close()
    return render_template('admin_citas.html', citas=citas)

# Logout
@app.route('/logout')
def logout():
    session.pop('autenticado', None)
    return redirect('/')


# Configuración del servidor SMTP (ejemplo con Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rauladrianga@gmail.com'        # <- cambia esto
app.config['MAIL_PASSWORD'] = 'wjgu eyfv yxmj mwmy'  # <- usa app password si usas Gmail
app.config['MAIL_DEFAULT_SENDER'] = 'tu_correo@gmail.com'  # <- igual al username

mail = Mail(app)


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
            email TEXT NOT NULL,       
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
    try:
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        fecha = request.form['fecha']
        hora = request.form['hora']

        conn = sqlite3.connect('citas.db')
        conn.execute('''
            INSERT INTO citas (nombre, edad, direccion, telefono,email, fecha, hora)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, edad, direccion, telefono, email, fecha, hora))
        conn.commit()
        conn.close()

        # Enviar correo de confirmación
        msg = Message('Confirmacion de cita medica',
                      recipients=[email])
        msg.body = f'''
Hola {nombre},

Tu cita ha sido registrada con exito.

Fecha: {fecha}
Hora: {hora}
Direccion: {direccion}

Gracias por usar nuestro sistema.
'''
        mail.send(msg)
        print(f"✅ Correo enviado a {email}")
    except Exception as e:
        print("❌ Error al agregar o enviar correo:", e)
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

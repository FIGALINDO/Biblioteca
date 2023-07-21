from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'  
db_path = 'biblioteca.db'  

# Con esto se crea la base de datos y la tablas si no existen
def create_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitante_id INTEGER NOT NULL,
            libro_id INTEGER NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion TEXT NOT NULL,
            FOREIGN KEY (solicitante_id) REFERENCES solicitantes (id),
            FOREIGN KEY (libro_id) REFERENCES libros (id)
        )
    ''')

    conn.commit()
    conn.close()

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Esta es la ruta para mostrar todos los solicitantes
@app.route('/solicitantes')
def solicitantes():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solicitantes')
    solicitantes = cursor.fetchall()
    conn.close()
    return render_template('solicitantes.html', solicitantes=solicitantes)

# La ruta para agregar un solicitante es la siguiente:
@app.route('/solicitantes/add', methods=['GET', 'POST'])
def agregar_solicitante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO solicitantes (nombre, email, telefono) VALUES (?, ?, ?)',
                       (nombre, email, telefono))
        conn.commit()
        conn.close()

        flash('Solicitante agregado correctamente', 'success')
        return redirect('/solicitantes')
    else:
        return render_template('agregar_solicitante.html')

# Por aquí está la ruta que permite editar un solicitante
@app.route('/solicitantes/edit/<int:solicitante_id>', methods=['GET', 'POST'])
def editar_solicitante(solicitante_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE solicitantes SET nombre = ?, email = ?, telefono = ? WHERE id = ?',
                       (nombre, email, telefono, solicitante_id))
        conn.commit()
        conn.close()

        flash('Solicitante actualizado correctamente', 'success')
        return redirect('/solicitantes')
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM solicitantes WHERE id = ?', (solicitante_id,))
        solicitante = cursor.fetchone()
        conn.close()

        if solicitante:
            return render_template('editar_solicitante.html', solicitante=solicitante)
        else:
            flash('Solicitante no encontrado', 'error')
            return redirect('/solicitantes')

# Ruta para eliminar un solicitante
@app.route('/solicitantes/delete/<int:solicitante_id>', methods=['POST'])
def eliminar_solicitante(solicitante_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM solicitantes WHERE id = ?', (solicitante_id,))
    conn.commit()
    conn.close()

    flash('Solicitante eliminado correctamente', 'success')
    return redirect('/solicitantes')

# Ruta para mostrar todos los libros
@app.route('/libros')
def libros():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    conn.close()
    return render_template('libros.html', libros=libros)

# Esta es la ruta que permite agregar un libro
@app.route('/libros/add', methods=['GET', 'POST'])
def agregar_libro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        stock = request.form['stock']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO libros (titulo, autor, stock) VALUES (?, ?, ?)',
                       (titulo, autor, stock))
        conn.commit()
        conn.close()

        flash('Libro agregado correctamente', 'success')
        return redirect('/libros')
    else:
        return render_template('agregar_libro.html')

# La ruta para editar un libro es la que se muestra a continuación:
@app.route('/libros/edit/<int:libro_id>', methods=['GET', 'POST'])
def editar_libro(libro_id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        stock = request.form['stock']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE libros SET titulo = ?, autor = ?, stock = ? WHERE id = ?',
                       (titulo, autor, stock, libro_id))
        conn.commit()
        conn.close()

        flash('Libro actualizado correctamente', 'success')
        return redirect('/libros')
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM libros WHERE id = ?', (libro_id,))
        libro = cursor.fetchone()
        conn.close()

        if libro:
            return render_template('editar_libro.html', libro=libro)
        else:
            flash('Libro no encontrado', 'error')
            return redirect('/libros')

# Esta es la ruta para eliminar un libro
@app.route('/libros/delete/<int:libro_id>', methods=['POST'])
def eliminar_libro(libro_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM libros WHERE id = ?', (libro_id,))
    conn.commit()
    conn.close()

    flash('Libro eliminado correctamente', 'success')
    return redirect('/libros')

# Por acá está la ruta para mostrar todos los préstamos
@app.route('/prestamos')
def prestamos():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT p.id, s.nombre, l.titulo, p.fecha_prestamo, p.fecha_devolucion '
                   'FROM prestamos p '
                   'JOIN solicitantes s ON p.solicitante_id = s.id '
                   'JOIN libros l ON p.libro_id = l.id')
    prestamos = cursor.fetchall()
    conn.close()
    return render_template('prestamos.html', prestamos=prestamos)

# Aquí va la ruta para agregar un préstamo
@app.route('/prestamos/add', methods=['GET', 'POST'])
def agregar_prestamo():
    if request.method == 'POST':
        solicitante_id = request.form['solicitante']
        libro_id = request.form['libro']
        fecha_prestamo = request.form['fecha_prestamo']
        fecha_devolucion = request.form['fecha_devolucion']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO prestamos (solicitante_id, libro_id, fecha_prestamo, fecha_devolucion) '
                       'VALUES (?, ?, ?, ?)', (solicitante_id, libro_id, fecha_prestamo, fecha_devolucion))
        conn.commit()
        conn.close()

        flash('Préstamo agregado correctamente', 'success')
        return redirect('/prestamos')
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM solicitantes')
        solicitantes = cursor.fetchall()

        cursor.execute('SELECT * FROM libros')
        libros = cursor.fetchall()

        conn.close()

        return render_template('agregar_prestamo.html', solicitantes=solicitantes, libros=libros)

# Esta es la ruta para editar un préstamo
@app.route('/prestamos/edit/<int:prestamo_id>', methods=['GET', 'POST'])
def editar_prestamo(prestamo_id):
    if request.method == 'POST':
        solicitante_id = request.form['solicitante']
        libro_id = request.form['libro']
        fecha_prestamo = request.form['fecha_prestamo']
        fecha_devolucion = request.form['fecha_devolucion']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE prestamos SET solicitante_id = ?, libro_id = ?, fecha_prestamo = ?, fecha_devolucion = ? '
                       'WHERE id = ?', (solicitante_id, libro_id, fecha_prestamo, fecha_devolucion, prestamo_id))
        conn.commit()
        conn.close()

        flash('Préstamo actualizado correctamente', 'success')
        return redirect('/prestamos')
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obtener datos del préstamo 
        cursor.execute('SELECT * FROM prestamos WHERE id = ?', (prestamo_id,))
        prestamo = cursor.fetchone()

        # Por acá se obtienen las listas de solicitantes y libros para el formulario
        cursor.execute('SELECT * FROM solicitantes')
        solicitantes = cursor.fetchall()

        cursor.execute('SELECT * FROM libros')
        libros = cursor.fetchall()

        conn.close()

        if prestamo:
            return render_template('editar_prestamo.html', prestamo=prestamo, solicitantes=solicitantes, libros=libros)
        else:
            flash('Préstamo no encontrado', 'error')
            return redirect('/prestamos')

# Esta es la ruta que permite eliminar un préstamo
@app.route('/prestamos/delete/<int:prestamo_id>', methods=['POST'])
def eliminar_prestamo(prestamo_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM prestamos WHERE id = ?', (prestamo_id,))
    conn.commit()
    conn.close()

    flash('Préstamo eliminado correctamente', 'success')
    return redirect('/prestamos')

if __name__ == '__main__':
    create_database()
    app.run(debug=True)

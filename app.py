from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                      r'DBQ=C:\Users\aldeb\OneDrive\Documentos\Taller15\TasksDB.accdb')

@app.route('/')
def index():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Tareas')
    tareas = cursor.fetchall()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        estado = 0
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Tareas (descripcion, estado) VALUES (?, ?)', (descripcion, estado))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/completar_tarea/<int:Id>')
def completar_tarea(Id):
    cursor = conn.cursor()
    cursor.execute('UPDATE Tareas SET estado = 1 WHERE Id = ?', (Id,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/eliminar_tarea/<int:Id>')
def eliminar_tarea(Id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Tareas WHERE Id = ?', (Id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

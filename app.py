from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontac'
mysql = MySQL(app)

# Seting
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contac')
    data = cur.fetchall()
    # print(data)
    return render_template('index.html', contacs=data)

@app.route('/add_contac', methods=['POST'])
def add_contac():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contac(nombre, apellido, telefono, email) VALUES (%s, %s, %s, %s)', (nombre, apellido, telefono, email))
        mysql.connection.commit()
        flash('Contacto agregado correctamente')
    return redirect(url_for('index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contac WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('editContac.html', contac = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contac
            SET nombre = %s,
                apellido = %s,
                email = %s,
                telefono = %s
            WHERE id = %s
            """, (nombre, apellido, email, telefono,  id)
        )
        mysql.connection.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('index'))
    

@app.route('/delete/<string:id>')
def delete_contac(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contac WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto removido correctamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
import hashlib
from random import randint
from flask import Flask, render_template, request, redirect, flash, session
from flaskext.mysql import MySQL
from datetime import timedelta

programa = Flask(__name__)
programa.secret_key = str(randint(10000, 99999))
programa.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
mysql = MySQL()
programa.config['MYSQL_DATABASE_HOST'] = 'localhost'
programa.config['MYSQL_DATABASE_PORT'] = 3306
programa.config['MYSQL_DATABASE_USER'] = 'root'
programa.config['MYSQL_DATABASE_PASSWORD'] = ''
programa.config['MYSQL_DATABASE_DB'] = 'consulta'
mysql.init_app(programa)

conexion = mysql.connect()
cursor = conexion.cursor()

@programa.route('/')
def index():
    return render_template("login.html")

@programa.route('/guardar', methods=['GET', 'POST'])
def guardar():
    if request.method == 'POST':
        campos = ['idusuario', 'nombre', 'contrasena', 'activo']

        valores = {}
        for campo in campos:
            if campo == 'activo':
                valores[campo] = 1
            else:
                valor = request.form.get(campo)
                valores[campo] = valor

        if all(valores.values()):  # Verificar si todos los valores están presentes
            contrasena = valores['contrasena']
            encriptada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()
            valores['contrasena'] = encriptada

            consulta = f"INSERT INTO usuarios ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(campos))})"
            valoresOrdenados = [valores[campo] for campo in campos]
            cursor.execute(consulta, valoresOrdenados)

            conexion.commit()

            flash("Los datos se han insertado correctamente.", "success")  # Mensaje flash de éxito
        else:
            # Si algún campo está vacío, se muestra un mensaje de error
            flash("Por favor, complete todos los campos.", "error")

        return redirect('/')

    else:
        return render_template('register.html')
    
@programa.route('/validationLogin', methods = ['POST'])
def validationLogin():
    if request.method == 'POST':
        idusuario = request.form.get('idusuario')
        contrasena = request.form.get('contrasena')

        encriptada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()

        # Establecer la conexión a la base de datos y obtener el cursor
        # Aquí deberías agregar tu código de conexión a la base de datos

        consulta = f"SELECT contrasena, nombre FROM usuarios WHERE idusuario = '{idusuario}'"

        cursor.execute(consulta)
        resultado = cursor.fetchall()
        conexion.commit()

        if len(resultado) > 0:
            if encriptada == resultado[0][0]:
                session["logueado"] = True
                session["user_id"] = idusuario
                session["user_name"] = resultado[0][1]
                return redirect('/principal')
            else:
                return render_template('login.html')
        else:
            return render_template('login.html')
        
@programa.route('/principal')
def principal():
    if session.get("logueado"):
        return render_template("principal.html")
    else:
        return render_template("login.html")
    
        
@programa.route('/medicos')
def medicos():
    if session.get("logueado"):
        consulta = "SELECT * FROM medicos WHERE activo = 1"

        cursor.execute(consulta)
        resultados = cursor.fetchall()
        conexion.commit()

        return render_template('/medicos.html', res = resultados)
    else:
        return render_template("login.html")

@programa.route('/agregaMedico')
def agregaMedico():
    if session.get("logueado"):
        return render_template('agregaMedico.html')
    else:
        return render_template("login.html")

@programa.route('/guardaMedico', methods = ['POST'])
def guardaMedico():
    if session.get("logueado"):
        id = request.form['txtId']
        nombre = request.form['txtNombre']
        especialidad = request.form['txtEspe']

        consultaMedicos = f"SELECT * FROM medicos WHERE idmedico = '{id}'"

        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(consultaMedicos)

        resultado = cursor.fetchone()

        conexion.commit()

        if not resultado:

            consulta = f"INSERT INTO medicos (idmedico, nombre, especialidad, activo) VALUES ('{id}','{nombre}','{especialidad}', 1)"

            cursor.execute(consulta)
            conexion.commit()

            return redirect('/medicos')
        
        else: 
            return render_template('agregaMedico.html' , men = 'ID de medico no disponible')
    else:
        return render_template("login.html")
    
@programa.route('/deleteMedico/<id>')
def deleteMedico(id):
    if session.get("logueado"):
        consulta = f"UPDATE medicos SET activo = 0 WHERE idmedico = '{id}'"
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        return redirect('/medicos')
    else:
        return render_template("login.html")

if __name__ == '__main__':
    programa.run(host='0.0.0.0', debug=True, port='8080')
########################################################################################
# import hashlib
# from flask import Flask, render_template, request, redirect, flash
# from flaskext.mysql import MySQL

# programa = Flask(__name__)
# programa.secret_key = 'clave_secreta' 
# mysql = MySQL()
# programa.config['MYSQL_DATABASE_HOST'] = 'localhost'
# programa.config['MYSQL_DATABASE_PORT'] = 3306
# programa.config['MYSQL_DATABASE_USER'] = 'root'
# programa.config['MYSQL_DATABASE_PASSWORD'] = ''
# programa.config['MYSQL_DATABASE_DB'] = 'consulta'
# mysql.init_app(programa)

# conexion = mysql.connect()
# cursor = conexion.cursor()

# @programa.route('/')
# def index():
#     return render_template("login.html")

# @programa.route('/guardar', methods=['GET', 'POST'])
# def guardar():
#     if request.method == 'POST':
#         campos = ['idusuario', 'nombre', 'contrasena', 'activo']

#         valores = {}
#         for campo in campos:
#             if campo == 'activo':
#                 valores[campo] = 1
#             else:
#                 valor = request.form.get(campo)
#                 valores[campo] = valor

#         if 'contrasena' in valores:
#             contrasena = valores['contrasena']
#             encriptada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()
#             valores['contrasena'] = encriptada

#             consulta = f"INSERT INTO usuarios ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(campos))})"
#             valoresOrdenados = [valores[campo] for campo in campos]
#             cursor.execute(consulta, valoresOrdenados)

#             conexion.commit()

#             flash("Los datos se han insertado correctamente.", "success")  # Mensaje flash de éxito

#         return redirect('/')

#     else:
#         return render_template('formulario.html')

# if __name__ == '__main__':
#     programa.run(host='0.0.0.0', debug=True, port='8080')











# import hashlib
# from flask import Flask, render_template, request, redirect, flash
# from flaskext.mysql import MySQL

# programa = Flask(__name__)
# programa.secret_key = 'clave_secreta' 
# mysql = MySQL()
# programa.config['MYSQL_DATABASE_HOST'] = 'localhost'
# programa.config['MYSQL_DATABASE_PORT'] = 3306
# programa.config['MYSQL_DATABASE_USER'] = 'root'
# programa.config['MYSQL_DATABASE_PASSWORD'] = ''
# programa.config['MYSQL_DATABASE_DB'] = 'consulta'
# mysql.init_app(programa)

# conexion = mysql.connect()
# cursor = conexion.cursor()

# @programa.route('/')
# def index():
#     return render_template("login.html")

# @programa.route('/guardar', methods=['GET', 'POST'])
# def guardar():
#     if request.method == 'POST':
#         campos = ['idusuario', 'nombre', 'contrasena', 'activo']

#         valores = {}
#         for campo in campos:
#             if campo == 'activo':
#                 valores[campo] = 1
#             else:
#                 valor = request.form.get(campo)
#                 valores[campo] = valor

#         if 'contrasena' in valores:
#             contrasena = valores['contrasena']
#             encriptada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()
#             valores['contrasena'] = encriptada

#             consulta = f"INSERT INTO usuarios ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(campos))})"
#             valoresOrdenados = [valores[campo] for campo in campos]
#             cursor.execute(consulta, valoresOrdenados)

#             conexion.commit()

#             flash("Los datos se han insertado correctamente.", "success")  # Mensaje flash de éxito

#         return redirect('/')

#     else:
#         return render_template('formulario.html')

# if __name__ == '__main__':
#     programa.run(host='0.0.0.0', debug=True, port='8080')


# idusuario = input("Digite id: ")
# nombre = input("Digite nombre: ")
# contrasena = input("Digite contraseña: ")
# cifrada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()

# sql = f"INSERT INTO usuarios (idusuario,nombre,contrasena,activo) VALUES ('{idusuario}','{nombre}','{cifrada}',1)"
# con = mysql.connect()
# cur = con.cursor()
# cur.execute(sql)
# con.commit()
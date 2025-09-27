from flask import Flask, render_template, request, redirect, flash, url_for,session
from consultas import consulta, insertar
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from collections import defaultdict
from decoradores import login_requerido
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('API_KEY')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def nombre_imagen(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    query = "SELECT nombre, apellido, foto, rol FROM desarrolladores"
    query2 ="SELECT e.id_emprendimiento AS id, e.nombre, e.logo, t.tecnico FROM emprendimientos e INNER JOIN tecnico t ON t.idtecnico = e.id_tecnico"
    desarrolladores = consulta(query)
    emprendimientos= consulta(query2)
    emprendimientos_por_tecnico=defaultdict(list)
    for emprendimiento in emprendimientos:
        tecnico=emprendimiento['tecnico']
        emprendimientos_por_tecnico[tecnico].append(emprendimiento)
    return render_template('index.html', desarrolladores=desarrolladores, emprendimientos=emprendimientos_por_tecnico)

@app.route('/emprendimiento/<int:cod>')
def emprendimiento(cod):
    query ="SELECT * FROM emprendimientos WHERE id_emprendimiento=%s"
    query2 ="SELECT CONCAT(nombre, ' ', apellido ) AS nombre, cargo, foto FROM emprendedores WHERE emprendimiento = %s"
    parametros=cod,
    emprendimientos= consulta(query,parametros)
    emprendedores= consulta(query2,parametros)
   
    return render_template('emprendimiento.html', emprendimientos=emprendimientos, emprendedores=emprendedores)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        aprendices={'1115732618','1093297547','1115732065','1115731358','1127917657','1115728076','1115730470','1115731435','1127914657','1115730794','1115731035','1115730837','1115729018','1115727634','1028784701','1115727407', '987564'}
        doc = request.form.get('doc')
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        celular = request.form.get('celular')
        password = request.form.get('password')
        confirm_password =  request.form.get('confirm_password')
        foto = request.files.get('foto')
        if doc in aprendices:
            if password != confirm_password:
                flash('Las contraseñas no coinciden.', 'error')
                return redirect(request.url)

            if foto and nombre_imagen(foto.filename):
                filename = secure_filename(foto.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                nuevo_nombre = f"{uuid.uuid4().hex}.{extension}"
                ruta_foto = os.path.join(app.config['UPLOAD_FOLDER'], nuevo_nombre)
                foto.save(ruta_foto)
            else:
                flash('Formato de imagen no permitido. Solo .webp', 'error')
                return redirect(request.url)

            query = "INSERT INTO desarrolladores (documento, nombre, apellido, password, celular, foto) VALUES (%s,%s,%s,%s,%s,%s)"
            password_hash=generate_password_hash(password)
            parametros = (doc, nombres, apellidos, password_hash, celular, nuevo_nombre)
            insertar(query,parametros)

            flash('Registro exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('No tienes permiso de crear una cuenta', 'error')
            return redirect(request.url)
    return render_template('crear_dev.html')


@app.route('/crear_emprendedor', methods=['GET', 'POST'])
@login_requerido
def crear_emprendedor():
    query = "SELECT id_emprendimiento AS id, nombre FROM emprendimientos "
    emprendimientos = consulta(query)
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        cargo = request.form.get('cargo')
        emprendimiento = int(request.form.get('emprendimiento'))
        foto = request.files.get('foto')


        if foto and nombre_imagen(foto.filename):
            filename = secure_filename(foto.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            nuevo_nombre = f"{uuid.uuid4().hex}.{extension}"
            ruta_foto = os.path.join(app.config['UPLOAD_FOLDER'], nuevo_nombre)
            foto.save(ruta_foto)
        else:
            flash('Formato de imagen no permitido. Solo .webp', 'error')
            return redirect(request.url)
        
        query="INSERT INTO emprendedores (nombre, apellido, cargo, foto, emprendimiento) VALUES (%s,%s,%s,%s,%s)"
        parametros =(nombres, apellidos,cargo,nuevo_nombre,emprendimiento)
        insertar(query, parametros)
        return redirect(url_for('index'))
    return render_template('crear_emprendedor.html', emprendimientos = emprendimientos)

@app.route('/crear_emprendimiento' , methods=['GET', 'POST'])
@login_requerido
def crear_emprendimiento():
    query="SELECT * FROM tecnico"
    tecnicos=consulta(query)
    if request.method == 'POST':
    
        nombre = request.form.get('nombre')
        slogan = request.form.get('slogan')
        contacto = request.form.get('contacto')
        descripcion = request.form.get('descripcion')
        mision = request.form.get('mision')
        vision = request.form.get('vision')
        objetivo= request.form.get('objetivos')
        foto = request.files.get('logo')
        producto = request.files.get('producto')
        
        tecnico = request.form.get('tecnico')


        if foto and nombre_imagen(foto.filename) and nombre_imagen(producto.filename):
            filename = secure_filename(foto.filename)
            nombre_archivo= secure_filename(producto.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            extension2 = nombre_archivo.rsplit('.', 1)[1].lower()
            nuevo_nombre = f"{uuid.uuid4().hex}.{extension}"
            nombre_producto =  f"{uuid.uuid4().hex}.{extension2}"
            ruta_foto = os.path.join(app.config['UPLOAD_FOLDER'], nuevo_nombre)
            ruta_foto_producto = os.path.join(app.config['UPLOAD_FOLDER'], nombre_producto)
            foto.save(ruta_foto)
            producto.save(ruta_foto_producto)
            
        else:
            flash('Formato de imagen no permitido. Solo .webp', 'error')
            return redirect(request.url)
        
        
        query = "INSERT INTO emprendimientos (nombre, slogan, mision, vision, objetivos, descripcion, logo, contacto, id_tecnico, foto_producto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        parametros = (nombre, slogan, mision, vision, objetivo, descripcion, nuevo_nombre, contacto, tecnico, nombre_producto)
        insertar(query, parametros)
        return redirect(url_for('index'))


    return render_template('crear_emprendimiento.html', tecnicos=tecnicos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        documento = request.form['documento']
        password = request.form['password']
        query = "SELECT documento, password, rol, nombre FROM desarrolladores WHERE documento = %s"
        parametros = (documento,)
        respuesta = consulta(query, parametros)

        if respuesta:
            usuario=respuesta[0]
            contra=usuario['password']
    
            if check_password_hash(contra, password):
                session['user'] = usuario['nombre']
                session['documento']=usuario['documento']
                session['rol']=usuario['rol']
                return redirect(url_for('index')) 
            else:
                flash('Contraseña incorrecta.', 'error')
        else:
            flash('Usuario no encontrado.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('documento', None)  
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('index')) 


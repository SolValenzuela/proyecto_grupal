from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.taller import Taller
from flask_app.models.horno import Horno


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/taller/hora')
def taller_hora_horno():
    talleres=Horno.get_taller_agenda()
    return render_template('taller_hora.html',talleres=talleres)


@app.route('/registro')
def registro():
    return render_template('registro_taller.html')



#ruta Post de formulario de registro de taller,guarda los datos del nuevo taller y redirige
@app.route('/procesar/taller', methods=['POST'])
def procesar_taller():
    is_valid= Taller.validar_usuario(request.form)
    print(is_valid)
    if not is_valid:
        print('No valido')
        return redirect('/registro')
    
    nuevo_usuario = {
        "nombre":request.form['nombre'],
        "direccion":request.form['direccion'],
        "comuna":request.form['comuna'],
        "email": request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password']),    
    }
    id = Taller.save(nuevo_usuario)
    if not id:
        flash("The email already exists.","register")
        return redirect('/login/taller')
    session['taller'] = request.form['nombre']
    session['taller_id'] = id
    return redirect('/crear/horno')


#ruta para loguearse
@app.route('/login/taller')
def login_taller():
    return render_template('login_taller.html')


# ruta Post de formulario login/taller,comprueba que taller existe,guarda datos de session y redirige
@app.route("/procesar/login/taller",methods=['POST'])
def procesar_login_taller():


    data = {
        "email": request.form['email']
    }
    taller = Taller.get_by_email(data)
    if not taller:
        flash("Email or password invalido","register")
        print('Email or password invalido","register')
        return redirect("/login/taller")
    
    if not bcrypt.check_password_hash(taller.password,request.form['password']):
        flash("Email or password invalido","register")
        return redirect("/login/taller")
    session['taller_id'] =taller.id
    session['taller']=taller.nombre
    
    return redirect('/listado/horno')



@app.route('/proximamente')
def proximamente():
    return render_template('proximamente.html')


#Ruta para desloguearse
@app.route('/logout/taller')
def close_session():
    session.clear()
    return redirect('/')





from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usuario import Usuario



from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 




@app.route('/registro/usuario')
def registro_usuario():
    return render_template('registro_usuario.html')



#ruta Post de formulario de registro de usuario,guarda los datos del nuevo usuario y redirige
@app.route('/procesar/usuario', methods=['POST'])
def procesar_usuario():
    is_valid= Usuario.validar_usuario(request.form)
    print(is_valid)
    if not is_valid:
        print('No valido')
        return redirect('/registro')
    
    nuevo_usuario = {
        "nombre":request.form['nombre'],
        "email": request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password']),    
    }
    id = Usuario.save(nuevo_usuario)
    if not id:
        flash("The email already exists.","register")
        return redirect('/login/taller/usuario')
    session['usuario'] = request.form['nombre']
    session['usuario_id'] = id
    return redirect('/')


#ruta para loguearse
@app.route('/login/taller/usuario')
def  login_taller_usuario():
        return render_template('login/taller_usuario.html')


# ruta Post de formulario login/taller,comprueba que usuario existe,guarda datos de session y redirige
@app.route("/procesar/login/taller/usuario",methods=['POST'])
def procesar_login_taller_usuario():


    data = {
        "email": request.form['email']
    }
    usuario = Usuario.get_by_email(data)
    if not usuario:
        flash("Email or password invalido","register")
        print('Email or password invalido","register')
        return redirect("/login/taller/usuario")
    
    if not bcrypt.check_password_hash(usuario.password,request.form['password']):
        flash("Email or password invalido","register")
        return redirect("/login/taller/usuario")
    session['usuario_id'] =usuario.id
    session['usuario']=usuario.nombre
    
    return redirect('/')




#Ruta para desloguearse
@app.route('/desloguearse')
def cerrar_session():
    session.clear()
    return redirect('/')




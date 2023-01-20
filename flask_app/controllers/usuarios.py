from flask_app import app
import requests
from flask import render_template,redirect,request,session,flash,abort
from flask_app.models.usuario import Usuario
from flask_app.controllers import comentarios,talleres


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

import os
import pathlib


from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

# app = Flask("Google Login App")
# app.secret_key = "CodeSpecialist.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID ="493495931521-8dhje2bsuoh28o69g0fbto635jsm1en0.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# @app.route("/")
# def index():
#     return "Hello World <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"



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
        return redirect('/login/usuario')
    session['usuario'] = request.form['nombre']
    session['usuario_id'] = id
    return redirect('/')


#ruta para loguearse sin cuenta google
@app.route('/login/usuario')
def  login_usuario():
        return render_template('login_usuario.html')


# ruta Post de formulario login/usuario,comprueba que usuario existe,guarda datos de session y redirige
@app.route("/procesar/login/usuario",methods=['POST'])
def procesar_login_usuario():


    data = {
        "email": request.form['email']
    }
    usuario = Usuario.get_by_email(data)
    if not usuario:
        flash("Email or password invalido","register")
        print('Email or password invalido","register')
        return redirect("/login/usuario")
    
    if not bcrypt.check_password_hash(usuario.password,request.form['password']):
        flash("Email or password invalido","register")
        return redirect("/login/usuario")
    session['usuario_id'] =usuario.id
    session['usuario']=usuario.nombre
    
    return redirect('/comentario')







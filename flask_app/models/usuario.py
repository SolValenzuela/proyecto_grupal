from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 


import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#nombre de la base de datos
db_name='ceramistas'

class Usuario:
    
    def __init__(self,data):
        self.id = data['id']
        self.nombre= data['nombre']
        self.email= data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    #guardar datos o insertar datos en la tabla (puede ser llamado create)
    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (nombre,email,password) VALUES (%(nombre)s,%(email)s,%(password)s);"
        results= connectToMySQL(db_name).query_db(query,data)
        return results


    #obtener todos los datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        usuarios =  connectToMySQL(db_name).query_db(query)

        usuario =[]
        for b in usuarios:
            usuario.append(cls(b))
        return usuario
    

    # obtener datos a través de email
    @classmethod
    def get_by_email(cls,data):
        
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(db_name).query_db(query,data)

        if len(results) < 1:
            return False
        return Usuario(results[0])  


#usado para guardar datos de la session
    @classmethod
    def buscar(cls, dato):
        query = "select * from usuarios where email = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(db_name).query_db(query, data)
        
        if len(results) < 1:
            return False
        return cls(results[0])


    #para utilizar el id de la session
    @classmethod
    def get_by_id(cls, taller_id):
        data = {
            "id": taller_id
        }
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        result = connectToMySQL(db_name).query_db(query,data)

        if len(result) < 1:
            return False
        return cls(result[0])

    

# para obtener un usuario después de la autentificación
    @classmethod
    def authenticated_user_by_input(cls, usuario_input):       
        valid = True
        existing_user = cls.get_by_email(usuario_input["email"])

        password_valid = True

        if not existing_user:
            valid = False           
        else:
            # recuperar la contraseña hasheada para comparar
            data = {
                "email": usuario_input["email"]
            }
            query = "SELECT password FROM usuarios WHERE email = %(email)s;"
            hashed_pw = connectToMySQL(db_name).query_db(query,data)[0]["password"]

            password_valid = bcrypt.check_password_hash(hashed_pw, usuario_input['password'])
        
            if not password_valid:
                valid = False
        if not valid:
            flash("Email o password invalido.", "register")
            return False
        return existing_user
    

    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        nombre=usuario['nombre'].strip()
        if nombre == '':
            flash('Nombre no puede estar vacío','register')
            is_valid= False
        if len(usuario['nombre']) <3:
            flash('Nombre debe contener al menos 2 caracteres','register')
            is_valid=False
        if not EMAIL_REGEX.match(usuario['email']):
            is_valid = False
            flash("Email inválido","register")
        if len(usuario['password']) < 6:
            is_valid = False
            flash('Password debe contener al menos 8 caracteres','register')
        if usuario['password'] != usuario['confirmar_password']:
            is_valid = False
            flash("Password no coincide","register")
        return is_valid



        
        

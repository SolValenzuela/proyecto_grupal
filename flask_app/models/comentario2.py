from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime,timedelta


db_name='ceramistas'
class Comentario:

    modelo = 'comentarios'
    campos = [ 'comentario','producto_id', 'usuarios_id']

    def __init__(self, data):
        self.id = data['id']
        self.producto_id = data['producto_id']
        self.comentario = data['comentario']
        self.usuario_id = data['usuarios_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_with_usuario(cls):
        query =f"SELECT * FROM {cls.modelo} JOIN usuarios ON usuarios.id ={cls.modelo}.usuarios_id;"
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query)
        print(results)
        all_data = []
        for data in results:
            all_data.append(cls(data))
        return all_data

    @classmethod
    def get_by_id_with_usuario(cls, id):
        query =f"SELECT * FROM {cls.modelo} JOIN usuarios ON usuarios.id ={cls.modelo}.usuarios_id WHERE comentario.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print(results)
        all_data = []
        for data in results:
            all_data.append(cls(data))
        return all_data

    @classmethod
    def update(cls, data):
        query = """UPDATE comentario 
                        SET producto_id=%(producto_id)s,
                        comentario = %(comentario)s,
                        usuario_id = %(usuario_id)s,
                        updated_at=NOW() 
                    WHERE id = %(id)s"""
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del {campo} no puede ser menor o igual {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True
        
        is_valid = cls.validar_largo(data, 'comentario', 10)
            
        return is_valid

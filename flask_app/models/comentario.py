from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime,timedelta


db_name='ceramistas'

class Comentario:
    
    def __init__(self,data):
        self.id = data['id']
        self.producto_id=data['producto_id']
        self.usuario_id= data['usuario_id']
        self.comentario= data['comentario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    


#guardar datos de comentario
    @classmethod
    def save(cls,data):
        query ="""
                INSERT INTO comentarios 
                (comentario_id,usuario_id,comentario)
                VALUES 
                (%(comentario_id)s,%(usuario_id)s,%(comentario)s);
            """
        results= connectToMySQL(db_name).query_db(query,data)
        return results
    

#obtener todos los comentarios
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comentarios;"
        comentarios =  connectToMySQL(db_name).query_db(query)

        comentario =[]
        for b in comentarios:
            comentario.append(cls(b))
        return comentario
    

#detalles del comentario por id
    @classmethod
    def get_all_by_id(cls,id):
        query = "SELECT * FROM comentarios where id=%(id)s;"
        data={'id':id}
        results =  connectToMySQL(db_name).query_db(query, data)
        return results
        



# /*mostrar todos los comentarios generados por un usuario*/
    @classmethod
    def show_horno_details(cls, usuario_id):
        query="""
                /*mostrar todos los comentarios generados por un usuario*/
               SELECT * from comentarios 
                WHERE usuario_id=%(usuario_id)s;
                """
        data={"usuario_id" : usuario_id}
        results =  connectToMySQL(db_name).query_db(query,data)
        return results



#update de comentario
    @classmethod
    def update(cls,data):
        query="""
            /* update de comentario*/
            UPDATE comentarios
            SET comentario=%(comentario)s
            WHERE id=%(id)s;
        """
        results=connectToMySQL(db_name).query_db(cls,data)
        return results



#elimina un comentario
    @classmethod
    def destroy(cls,data):
        data={'id':data}
        query= "DELETE from comentarios WHERE id=%(id)s;"
        results=connectToMySQL(db_name).query_db(query,data)
        return results   

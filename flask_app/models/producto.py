from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime,timedelta


db_name='ceramistas'

class Producto:
    
    def __init__(self,data):
        self.id = data['id']
        self.nombre=data['nombre']
        self.autor= data['autor']
        self.descripcion= data['descripcion']
        self.precio= data['precio']
        self.taller_id= data['taller_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    


#guardar datos de producto
    @classmethod
    def save(cls,data):
        query ="""
                INSERT INTO productos 
                (nombre,autor,descripcion,precio,taller_id)
                VALUES 
                (%(nombre)s,%(autor)s,%(descripcion)s,%(precio)s,%(taller_id)s);
            """
        results= connectToMySQL(db_name).query_db(query,data)
        return results
    

#obtener todos los productos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM productos;"
        productos =  connectToMySQL(db_name).query_db(query)

        producto =[]
        for b in productos:
            producto.append(cls(b))
        return producto
    

#detalles del producto por id
    @classmethod
    def get_all_by_id(cls,id):
        query = "SELECT * FROM productos where id=%(id)s;"
        data={'id':id}
        results =  connectToMySQL(db_name).query_db(query, data)
        return results
        



# /*mostrar todos los productos generados por un taller*/
    @classmethod
    def get_all_products_by_taller(cls, taller_id):
        query="""
                /*mostrar todos los productos generados por un taller*/
               SELECT * from productos 
                WHERE taller_id=%(taller_id)s;
                """
        data={"taller_id" : taller_id}
        results =  connectToMySQL(db_name).query_db(query,data)
        return results



#update de producto
    @classmethod
    def update(cls,data):
        query="""
            /* update de producto*/
            UPDATE productos
            SET nombre=%(nombre)s, autor=%(autor)s,descripcion=%(descripcion)s,precio=%(precio)s
            WHERE id=%(id)s;
        """
        results=connectToMySQL(db_name).query_db(cls,data)
        return results





#elimina un producto
    @classmethod
    def destroy(cls,data):
        data={'id':data}
        query= "DELETE from productos WHERE id=%(id)s;"
        results=connectToMySQL(db_name).query_db(query,data)
        return results   

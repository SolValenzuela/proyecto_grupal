from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime,timedelta


db_name='ceramistas'

class Horno:
    
    def __init__(self,data):
        self.id = data['id']
        self.nombre=data['nombre']
        self.temperatura_min= data['temperatura_min']
        self.temperatura_max= data['temperatura_max']
        self.alto= data['alto']
        self.ancho= data['ancho']
        self.fondo= data['fondo']
        self.costo_bandeja= data['costo_bandeja']
        self.costo_medio_horno= data['costo_medio_horno']
        self.costo_horno_completo= data['costo_horno_completo']
        self.observaciones=data['observaciones']
        self.taller_creador_id=data['taller_creador_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    


#guardar datos de horno
    @classmethod
    def save(cls,data):
        query ="""
                INSERT INTO hornos 
                (nombre,temperatura_min,temperatura_max,ancho,alto,fondo,costo_bandeja,costo_medio_horno,costo_horno_completo,observaciones,taller_creador_id)
                VALUES 
                (%(nombre)s,%(temperatura_min)s,%(temperatura_max)s,%(ancho)s,%(alto)s,%(fondo)s,%(costo_bandeja)s,%(costo_medio_horno)s,%(costo_horno_completo)s,%(observaciones)s,%(taller_creador_id)s);
            """
        results= connectToMySQL(db_name).query_db(query,data)
        return results
    

#obtener todos los hornos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM hornos;"
        hornos =  connectToMySQL(db_name).query_db(query)

        horno =[]
        for b in hornos:
            horno.append(cls(b))
        return horno
    

#detalles del horno por id
    @classmethod
    def get_all_by_id(cls,id):
        query = "SELECT * FROM hornos where id=%(id)s;"
        data={'id':id}
        results =  connectToMySQL(db_name).query_db(query, data)
        return results
        


# /*mostrar todos los hornos generados por un taller y ordenados por disponibilidad de agenda*/
    @classmethod
    def show_horno_details_by_id(cls, taller_id):
        query="""
                /*mostrar todos los hornos generados por un taller*/
                SELECT h.id,h.nombre,h.temperatura_min ,h.temperatura_max ,h.alto ,h.ancho ,h.fondo ,h.costo_bandeja ,h.costo_medio_horno ,h.costo_horno_completo ,h.observaciones,
                    h.taller_creador_id,coalesce(min(fecha_inicio),'Sin disponibilidad') fecha_inicio, coalesce(min(hora_inicio),'-') hora_inicio, coalesce(hora_termino,'-') hora_termino
                FROM hornos h
                LEFT JOIN agendas a
                ON h.id = a.horno_id
                AND a.fecha_inicio > CURRENT_DATE() - 1
                AND a.agendada = 0
                WHERE h.taller_creador_id = %(taller_id)s
                GROUP BY h.id,h.nombre,h.temperatura_min ,h.temperatura_max ,h.alto ,h.ancho ,h.fondo ,h.costo_bandeja ,h.costo_medio_horno ,h.costo_horno_completo ,h.observaciones,h.taller_creador_id
                ORDER BY fecha_inicio, hora_inicio ASC;
                """
        data={"taller_id" : taller_id}
        results =  connectToMySQL(db_name).query_db(query,data)
        return results


# /*mostrar todos los hornos generados por un taller y ordenados por disponibilidad de agenda*/
    @classmethod
    def show_agenda_horno_by_id(cls, taller_id):
        query="""
                /*Muestra todas las hora por horno */
                SELECT h.id,a.id,h.nombre,h.temperatura_min ,h.temperatura_max ,h.alto ,h.ancho ,h.fondo ,h.costo_bandeja ,h.costo_medio_horno ,h.costo_horno_completo ,h.observaciones,
                    h.taller_creador_id,coalesce(fecha_inicio,'Sin disponibilidad') fecha_inicio, coalesce(hora_inicio,'-') hora_inicio, coalesce(hora_termino,'-') hora_termino
                FROM hornos h
                LEFT JOIN agendas a
                ON h.id = a.horno_id
                AND a.fecha_inicio > CURRENT_DATE() - 1
                AND a.agendada = 0
                WHERE h.taller_creador_id = %(taller_id)s
                ORDER BY fecha_inicio, hora_inicio ASC;
                """
        data={"taller_id" : taller_id}
        results =  connectToMySQL(db_name).query_db(query,data)
        return results

# /*mostrar todos los hornos generados por un taller*/
    @classmethod
    def show_horno_details(cls, horno_id):
        query="""
                /*mostrar todos los hornos generados por un taller*/
               SELECT * from hornos 
                WHERE taller_creador_id=%(taller_id)s;
                """
        data={"horno_id" : horno_id}
        results =  connectToMySQL(db_name).query_db(query,data)
        return results


#muestra la lista de talleres por disponibilidad horaria en orden asc
    @classmethod
    def get_taller_agenda(cls):

        query = """ SELECT t.id, t.nombre, t.direccion, t.comuna , t.email, coalesce(min(fecha_inicio),'Sin disponibilidad') fecha_inicio, coalesce(min(hora_inicio),'-') hora_inicio
                    FROM talleres t 
                    LEFT JOIN agendas a
                    ON t.id = a.taller_horno 
                    AND a.fecha_inicio > CURRENT_DATE() - 1
                    AND a.agendada = 0
                    GROUP BY t.id, t.nombre, t.direccion, t.comuna , t.email
                    ORDER BY fecha_inicio, hora_inicio ASC"""

        result = connectToMySQL(db_name).query_db(query)

        return result


#todos los hornos ordenados por disponibilidad de agenda con hora más próxima
    @classmethod
    def get_all_hornos_with_agenda(cls):
        query=  """
                /* todos los hornos ordenados por disponibilidad de agenda con hora más próxima*/
                SELECT h.id,h.nombre,t.id, t.nombre as nombre_taller,h.temperatura_min ,h.temperatura_max ,h.alto ,h.ancho ,h.fondo ,h.costo_bandeja ,h.costo_medio_horno ,h.costo_horno_completo ,h.observaciones,h.taller_creador_id,a.horno_id, coalesce(min(fecha_inicio),'Sin disponibilidad') fecha_inicio,  min(hora_inicio) hora_inicio
                FROM hornos h
                INNER JOIN talleres t
                ON h.taller_creador_id = t.id
                LEFT JOIN agendas a
                ON h.id = a.horno_id
                AND a.fecha_inicio > CURRENT_DATE() - 1
                AND a.agendada = 0
                GROUP BY h.id,h.nombre,h.temperatura_min ,h.temperatura_max ,h.alto ,h.ancho ,h.fondo ,h.costo_bandeja ,h.costo_medio_horno ,h.costo_horno_completo ,h.observaciones,h.taller_creador_id
                ORDER BY fecha_inicio, hora_inicio ASC;
                """
        results=connectToMySQL(db_name).query_db(query)
        return results


#mostrar los hornos ordenados por precio de menor a mayor
    @classmethod
    def precio_menor(cls):
        query="""
                /* Hornos con horas mas proximas ordenada por costos*/
                SELECT h.id,h.nombre,t.nombre as nombre_taller,h.temperatura_min ,h.temperatura_max ,h.alto ,h.ancho ,h.fondo ,h.costo_bandeja ,h.costo_medio_horno ,h.costo_horno_completo ,h.observaciones,h.taller_creador_id,coalesce(min(fecha_inicio),'Sin disponibilidad') fecha_inicio, min(hora_inicio) hora_inicio
                FROM hornos h
                INNER JOIN talleres t
                ON h.taller_creador_id = t.id
                LEFT JOIN agendas a
                ON h.id = a.horno_id
                AND a.fecha_inicio > CURRENT_DATE() - 1
                AND a.agendada = 0
                /*WHERE h.taller_creador_id = 5*/
                GROUP BY h.id,h.nombre,h.temperatura_min ,h.temperatura_max ,h.alto ,h.ancho ,h.fondo ,h.costo_bandeja ,h.costo_medio_horno ,h.costo_horno_completo ,h.observaciones,h.taller_creador_id
                ORDER BY  costo_bandeja ASC;
                """
        results=connectToMySQL(db_name).query_db(query)
        return results


#muestra todas las horas disponibles por horno
    @classmethod
    def all_hours_by_horno(cls,taller_id):
        query="""
                /*Muestra todas las hora por horno */
                SELECT h.id horno_id,a.id,h.nombre,h.temperatura_min ,h.temperatura_max ,h.alto ,h.ancho ,h.fondo ,h.costo_bandeja ,h.costo_medio_horno ,h.costo_horno_completo ,h.observaciones,
                    h.taller_creador_id,coalesce(fecha_inicio,'Sin disponibilidad') fecha_inicio, coalesce(hora_inicio,'-') hora_inicio, coalesce(hora_termino,'-') hora_termino
                FROM hornos h
                LEFT JOIN agendas a
                ON h.id = a.horno_id
                AND a.fecha_inicio > CURRENT_DATE() - 1
                AND a.agendada = 0
                WHERE h.taller_creador_id = %(taller_id)s
                ORDER BY fecha_inicio, hora_inicio ASC;
                """
        data = {'taller_id': taller_id}
        results=connectToMySQL(db_name).query_db(query, data)
        return results


#update de horno
    @classmethod
    def update(cls,data):
        query="""
            /* update de horno*/
            UPDATE hornos
            SET nombre=%(nombre)s, temperatura_min=%(temperatura_min)s,temperatura_max=%(temperatura_max)s,alto=%(alto)s,ancho=%(ancho)s,
                fondo=%(fondo)s,costo_bandeja=%(costo_bandeja)s,costo_medio_horno=%(costo_medio_horno)s,costo_horno_completo=%(costo_horno_completo)s,
                observaciones=%(observaciones)s
            WHERE id=%(id)s;
        """
        results=connectToMySQL(db_name).query_db(query,data)
        return results



#elimina un horno
    @classmethod
    def destroy(cls,data):
        data={'id':data}
        query= "DELETE from hornos WHERE id=%(id)s;"
        results=connectToMySQL(db_name).query_db(query,data)
        return results   

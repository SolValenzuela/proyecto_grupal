from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from datetime import datetime


db_name='ceramistas'

class Agenda:
    
    def __init__(self,data):
        self.id = data['id']
        self.fecha_inicio= data['fecha_inicio']
        self.hora_inicio=data['hora_inicio']
        self.hora_termino=data['hora_termino']
        self.taller_horno= data['taller_horno']
        self.agendada= data['agendada']
        self.email= data['email']
        self.telefono= data['telefono']
        self.horno_id=data['horno_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


#guardar los datos de la agenda
    @classmethod
    def save(cls,data):
        query = "INSERT INTO agendas (fecha_inicio,hora_inicio,hora_termino,taller_horno,horno_id,agendada) VALUES (%(fecha_inicio)s,%(hora_inicio)s,%(hora_termino)s,%(taller_horno)s,%(horno_id)s,%(agendada)s);"
        results= connectToMySQL(db_name).query_db(query,data)
        return results
    

#obtener todos los datos de la agenda
    @classmethod
    def get_agenda_by_id(cls, id):
        query = '''SELECT fecha_inicio, hora_inicio, hora_termino, h.nombre nombre_horno, t.nombre nombre_taller, t.direccion, t.comuna 
                    FROM agendas a
                    INNER JOIN hornos h
                    ON a.horno_id = h.id
                    INNER JOIN talleres t
                    ON t.id = a.taller_horno
                    WHERE a.id = %(id)s;'''
        data = { 'id' : id}
        agendas =  connectToMySQL(db_name).query_db(query, data)

        return agendas


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM agendas;"
        agendas =  connectToMySQL(db_name).query_db(query)

        agenda =[]
        for b in agendas:
            agenda.append(cls(b))
        return agenda

#selecciona los horarios disponibles por el taller creador
    @classmethod
    def get_by_id_user_creator(cls,taller_horno):
        data={
            'taller_horno':taller_horno
        }
        query = """
                /*selecciona horario por taller creador*/
                SELECT * FROM agendas 
                WHERE taller_horno=%(taller_horno)s;"""

        result =  connectToMySQL(db_name).query_db(query,data)
        return result


#selecciona los horarios disponibles del horno
    @classmethod
    def get_by_horno_id(cls,horno_id):
        data={
            'horno_id':horno_id
        }
        query = """
                /*selecciona horario por id de horno*/
                SELECT * FROM agendas 
                WHERE horno_id=%(horno_id)s AND agendada = 0;"""

        result =  connectToMySQL(db_name).query_db(query,data)
        return result


#actualizar estado de reserva
    @classmethod
    def reservar_hora(cls,data):
        query= """
                /* query para agendar las horas*/
                UPDATE agendas
                set agendada = %(agendada)s ,    /* marca para agendar */
                    email = %(email)s,
                    telefono = %(telefono)s
                WHERE id = %(id)s; /* id de la agenda*/
                """
        result=connectToMySQL(db_name).query_db(query,data)
        return result



#elimina una hora
    @classmethod
    def destroy(cls,data):
        data={'id':data}
        query= "DELETE from agendas WHERE id=%(id)s;"
        results=connectToMySQL(db_name).query_db(query,data)
        return results   





#validar fechas disponibles
    @staticmethod
    def validar_agenda(fecha):
        is_valid = True
        fecha_inicio=fecha['fecha_inicio'].strip()
        if fecha_inicio == '':
            flash('fecha de inicio no puede estar vacía','error')
            is_valid= False
        if len(fecha['fecha_inicio']) <1:
            flash('fecha de inicio no puede estar vacía','error')
            is_valid=False
        hora_inicio= fecha['hora_inicio'].strip()
        if hora_inicio == '':
            flash('hora de inicio no puede estar vacía','error')
            is_valid= False
        if len(fecha['hora_inicio']) <2:
            flash('Hora de inicio no puede estar vacía','error')
            is_valid= False
        hora_termino= fecha['hora_termino'].strip()
        if hora_termino == '':
            flash('Hora de termino no puede estar vacía','error')
            is_valid= False
        if len(fecha['hora_termino']) <2:
            flash('Hora de termino no puede estar vacía','error')
            is_valid= False
        fecha_inicio=fecha['fecha_inicio'] 
        if fecha_inicio < datetime.now().strftime("%Y-%m-%d"):
            flash('Fecha debe ser igual o mayor a la actual','error')
            is_valid=False
            
        return is_valid
    

    @staticmethod
    def validar_datos_reserva(reserva):
        is_valid=True
        email=reserva['email'].strip()
        if email == '':
            flash('Email no puede estar vacío','error')
            is_valid= False
        if len(reserva['email']) <1:
            flash('Email no puede estar vacío','error')
            is_valid=False
        # telefono=reserva['telefono'].strip()
        # if telefono == '':
        #     flash('Teléfono no puede estar vacío','error')
        #     is_valid= False
        # # if len(reserva['telefono']) ==12:
        # #     flash('El formato es +56911111111','error')
        #     is_valid=False
        return is_valid



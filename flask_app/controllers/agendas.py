from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for
from flask_app.models.taller import Taller
from flask_app.models.horno import Horno
from flask_app.models.agenda import Agenda
from flask_app.controllers import talleres

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText







#ruta para procesar y guardar los datos de la agenda
@app.route('/procesar/agenda/<horno_id>', methods=['POST'])
def procesar_agenda(horno_id):
    if 'taller_id' not in session:
        flash('Primero tienes que registrarte', 'register')
        return redirect('/login')

    hora_in=request.form['hora_inicio']+':'+request.form['init_min']+':00'
    hora_fin=request.form['hora_termino']+':'+request.form['init_min']+':00'
    print (f"horno procesado en procesar/agenda:  { horno_id }") 
    data={
        'fecha_inicio':request.form['fecha_inicio'],
        'hora_inicio':hora_in,
        'hora_termino':hora_fin,
        'taller_horno':session['taller_id'],
        'horno_id':horno_id,
        'agendada':0
    }
    validating=Agenda.validar_agenda(data)
    if not validating:
        flash('Error al crear la fecha','error')
        return redirect(f'/crear/agenda/{horno_id}')
    else:
        flash('Fecha agregada con éxito','success')
    Agenda.save(data)
    return redirect(f'/crear/agenda/{horno_id}')




#reservar horno
@app.route('/reserva/horno/<horno_id>')
def reserva_horno(horno_id):
    horarios=Agenda.get_by_horno_id(horno_id)
    detalles=Horno.get_all_hornos_with_agenda()
    # reservas=Agenda.reservar_hora(data)
    return render_template('reserva_horno.html', horarios=horarios,detalles=detalles)




# ruta post para procesar y guardar la reserva de hora
@app.route('/procesar/reserva/<id>' , methods=['POST'])
def procesar_reserva(id):
    
    data={
        'id': id,
        'email':request.form['email'],
        'telefono':request.form['telefono'],
        'agendada':1
    }

    # validating=Agenda.validar_datos_reserva(data)
    # if not validating:
    #     flash('Error al crear la reserva','error')
    #     return redirect('/detalles/reserva/<id>')
    # else:
    #     flash('Reserva con éxito','success')
    print(f"Revisar paso por procesar reserva { data } ")
    Agenda.reservar_hora(data)

    #agregar envío de mail 
    print(f"id de agenda para buscar la información : { id }")
    data = Agenda.get_agenda_by_id(id)
    print(f"datos para email : { data }")

    envio_mail(request.form['email'], data)

    return redirect('/reserva/confirmada')



#ruta para hacer reserva donde se deben ingresar los datos de contacto
@app.route('/detalles/reserva/<id>')
def detalles_reserva(id):
    #detalles_reserva=Agenda.reservar_hora(id)
    return render_template('confirma_reserva.html', id = id)


#ruta que muestra template de confirmación de hora reservada
@app.route('/reserva/confirmada')
def reserva_confirmada():
    return render_template('reserva_confirmada.html')




#arriendo de horno directo desde index,lista todos los hornos (pertenece a agenda)
@app.route('/arriendo/horno')
def arriendo_horno():
    hornos_agendas=Horno.get_all_hornos_with_agenda()
    return render_template('hornos_agenda.html',hornos_agendas=hornos_agendas)




#ruta para eliminar horas
@app.route('/destroy/agenda/<id>')
def destroy_agenda(id):
    if 'taller_id' not in session:
        flash('Primero tienes que loguearte', 'register')
        return redirect('/login')
    Agenda.destroy(id)
    return redirect('/listado/horno')



#para enviar mail 
def envio_mail(mail, datos):
    mail_content = f'''Estimado,

Tienes una reserva en el taller { datos[0].get('nombre_taller')} horno { datos[0].get('nombre_horno')} 

Fecha : { datos[0].get('fecha_inicio') }
Hora inicio : { datos[0].get('hora_inicio') }
Hora termino : { datos[0].get('hora_termino') }
Direccion : { datos[0].get('direccion')}
Comuna : { datos[0].get('comuna')}
'''
    #The mail addresses and password
    sender_address = 'sovalenz@gmail.com'
    sender_pass = 'sjrilesiexefyyec'
    receiver_address = mail
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Tienes una reserva para horno'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for
from flask_app.models.taller import Taller
from flask_app.models.horno import Horno
from flask_app.models.agenda import Agenda
from flask_app.controllers import talleres,agendas


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText





@app.route('/about')
def about():
    return render_template('about.html')


#ruta para crear el horno
@app.route('/crear/horno')
def crear_horno():
    if 'taller_id' not in session:
        flash('Primero tienes que registrarte', 'register')
        return redirect('/login/taller')
    return render_template('crear_horno.html')



# ruta post que procesa y guarda los datos del horno
@app.route('/procesar/horno' , methods=['post'])
def procesar_horno():
    if 'taller_id' not in session:
        flash('Primero tienes que registrarte', 'register')
        return redirect('/login/taller')
    data={
        'nombre':request.form['nombre'],
        'temperatura_min': request.form['temperatura_min'],
        'temperatura_max': request.form['temperatura_max'],
        "alto" : request.form['alto'],
        'ancho': request.form['ancho'],
        'fondo': request.form['fondo'],
        'costo_bandeja': request.form['costo_bandeja'],
        'costo_medio_horno': request.form['costo_medio_horno'],
        'costo_horno_completo': request.form['costo_horno_completo'],
        'observaciones': request.form['observaciones'],
        'taller_creador_id':session['taller_id']
    }
    horno_id=Horno.save(data)
    print (f"horno procesado { horno_id }")
    return redirect(url_for('crear_agenda', horno_id = horno_id))



#ruta para crear las horas de la agenda
@app.route('/crear/agenda/<horno_id>')
def crear_agenda(horno_id):
    if 'taller_id' not in session:
        flash('Primero tienes que registrarte', 'register')
        return redirect('/login/taller')
    return render_template('crear_agenda.html', horno_id=horno_id)



@app.route('/view/<taller_id>')
def details(taller_id):
    if 'taller' not in session:
        flash('Primero tienes que loguearte', 'register')
        return redirect('/login/taller')
    data={
        'taller_id':taller_id
    }
    detalle_hornos=Horno.show_horno_details_by_id(taller_id)
    talleres=Taller.get_by_id(taller_id)
    return render_template('show_horno_details.html',detalle_hornos=detalle_hornos,talleres=talleres)





#última modificación muestra todas las horas disponibles por horno
#listado  hornos del taller que permite agregar horas y eliminar horno
@app.route('/listado/horno')
def horas_by_horno():
    taller_id = session['taller_id'] 
    if 'taller_id' not in session:
        flash('Primero tienes que loguearte', 'register')
        return redirect('/login/taller')
    horarios=Horno.all_hours_by_horno(taller_id)
    return render_template('horas_by_horno.html', horarios=horarios)




#listado  hornos del taller que permite agregar horas y eliminar horno
@app.route('/actualiza/horno')
def actualiza_horno():
    taller_id = session['taller_id'] 
    if 'taller_id' not in session:
        flash('Primero tienes que loguearte', 'register')
        return redirect('/login/taller')
    horarios=Agenda.get_by_horno_id(taller_id)
    #detalles_actualizar=Horno.show_horno_details_by_id(taller_id)
    detalles_actualizar=Horno.show_agenda_horno_by_id(taller_id)
    return render_template('actualiza_horno.html',detalles_actualizar=detalles_actualizar,horarios=horarios)




#ruta para actualizar horno
@app.route('/actualiza/horno/<id>')
def actualizar_horno_by_id(id):
    return render_template('actualiza_horno_id.html')



#ruta Post para procesar update del horno
@app.route('/procesar/actualizar/horno', methods=['POST'])
def procesar_actualizar():
    if 'taller' not in session:
        flash('Primero tienes que loguearte', 'register')
        return redirect('/login/taller')
    data={
        'nombre':request.form['nombre'],
        'temperatura_min': request.form['temperatura_min'],
        'temperatura_max': request.form['temperatura_max'],
        "alto" : request.form['alto'],
        'ancho': request.form['ancho'],
        'fondo': request.form['fondo'],
        'costo_bandeja': request.form['costo_bandeja'],
        'costo_medio_horno': request.form['costo_medio_horno'],
        'costo_horno_completo': request.form['costo_horno_completo'],
        'observaciones': request.form['observaciones'],
        'taller_creador_id':session['taller_id']
    }
    
    new_horno=Horno.update(data)
    if not new_horno:
        flash('Error al actualizar horno','error')
        return redirect(f'/actualiza/horno/{id}')
    else:
        flash('Horno actualizado con éxito','success')
    return redirect('/listado/horno')


#detalle taller
@app.route('/detalle/taller/<horno_id>')
def detalle_taller(horno_id):
    detalles=Horno.get_all_by_id(horno_id)
    return render_template('detalle_taller.html',detalles=detalles)



# #arriendo de horno directo desde index,lista todos los hornos
# @app.route('/arriendo/horno')
# def arriendo_horno():
#     hornos_agendas=Horno.get_all_hornos_with_agenda()
#     return render_template('hornos_agenda.html',hornos_agendas=hornos_agendas)



#ruta que muestra los hornos ordenados por precio de menor a mayor
@app.route('/precio/menor')
def precio_menor():
    precios=Horno.precio_menor()
    return render_template('precio_menor.html',precios=precios)







#ruta para eliminar un horno
@app.route('/destroy/horno/<id>')
def destroy_horno(id):
    if 'taller' not in session:
        flash('Primero tienes que loguearte', 'register')
        return redirect('/login/taller')
    Horno.destroy(id)
    return redirect('/listado/horno/<taller_id>')






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
    session.login_taller(sender_address, sender_pass) #login/taller with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
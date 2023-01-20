from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for
from flask_app.models.comentario import Comentario
from flask_app.controllers import talleres,agendas

@app.route('/comentario')
def comentario():
    if 'usuario_id' not in session:
        return redirect('/login/usuario')
    return render_template('comentarios/comentario.html', comentarios = Comentario.get_all_with_usuario())

@app.route('/comentario/<int:id>')
def ver_comentario(id):
    if 'usuario_id' not in session:
        return redirect('/login/usuario')
    comentario = Comentario.get_by_id_with_usuario(id)[0]
    return render_template('comentarios/comentario.html', comentario=comentario)

@app.route('/comentario/nuevo')
def nuevo_comentario():
    # if 'usuario_id' not in session:
    #     return redirect('/login_usuario')
    return render_template('nuevo_comentario.html')

@app.route('/procesar_comentario', methods=['POST'])
def process_comentario():
    print(request.form)
    if not Comentario.validar(request.form):
        return redirect ('comentario/comentario')

    nuevo_comentario = { 
        'producto_id' : request.form ['producto_id'], #agregué esto
        'comentario' : request.form ['comentario'],
        'usuarios_id': session ['usuario_id']
    }
    comentario = Comentario.save(nuevo_comentario)
    if comentario == False:
            flash('Algo salió mal con la creación', 'error')
            return redirect('/comentario/nuevo')
    print(comentario)
    return redirect('/comentario')

from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.taller import Taller
from flask_app.models.producto import Producto
from flask_app.controllers import talleres



#ruta para crear el producto
@app.route('/publica/producto')
def publica_producto():
    if 'taller_id' not in session:
        flash('Primero tienes que registrarte', 'register')
        return redirect('/login/taller')
    return render_template('publica_producto.html')



# ruta post que procesa y guarda los datos del producto
@app.route('/procesar/producto' , methods=['post'])
def procesar_producto():
    if 'taller_id' not in session:
        flash('Primero tienes que registrarte', 'register')
        return redirect('/login/taller')
    data={
        'nombre':request.form['nombre'],
        'autor': request.form['autor'],
        'descripcion': request.form['descripcion'],
        "precio" : request.form['precio'],
        'taller_id':session['taller_id']
    }
    new_product=Producto.save(data)
    if not new_product:
        flash('Error al crear el producto','register')
        redirect('/publica/producto')

    return redirect('/productos')


@app.route('/productos')
def mostrar_productos():
    return render_template('mostrar_productos.html')

# #ruta para actualizar producto
# @app.route('/actualiza/producto/<id>')
# def actualizar_horno_by_id(id):
#     return render_template('actualiza_horno_id.html')



# #ruta Post para procesar update del producto
# @app.route('/procesar/actualizar/producto', methods=['POST'])
# def procesar_actualizar():
#     if 'taller' not in session:
#         flash('Primero tienes que loguearte', 'register')
#         return redirect('/login/taller')
#     data={
#         'nombre':request.form['nombre'],
#         'autor': request.form['autor'],
#         'descripcion': request.form['descripcion'],
#         "precio" : request.form['precio'],
#         'taller_id':session['taller_id']
#     }
    
#     new_horno=Producto.update(data)
#     if not new_horno:
#         flash('Error al actualizar producto','error')
#         return redirect(f'/actualiza/producto/{id}')
#     else:
#         flash('Horno actualizado con éxito','success')
#     return redirect('/listado/producto')





# #ruta que muestra los hornos ordenados por precio de menor a mayor
# @app.route('/producto/precio/menor')
# def producto_precio_menor():
#     precios=Horno.precio_menor()
#     return render_template('precio_menor.html',precios=precios)




#ruta para eliminar un producto
@app.route('/destroy/producto/<id>')
def destroy_producto(id):
    if 'taller' not in session:
        flash('Primero tienes que loguearte', 'register')
        return redirect('/login/taller')
    Producto.destroy(id)
    return redirect('/listado/producto/<taller_id>')



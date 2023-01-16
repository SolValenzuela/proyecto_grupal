from flask_app import app

from flask_app.controllers import talleres,hornos,agendas,usuarios,productos










if __name__=="__main__":
    app.run(debug=True)